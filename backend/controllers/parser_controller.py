import re

from bs4 import BeautifulSoup as bs
from bs4 import ResultSet
from fastapi import HTTPException, status
from httpx import AsyncClient, Response
from models.article import Article
from models.project import Project
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.cloudflare_handler import cloudflare_decode_email
from utils.request_client import get_request_client
from utils.url_handler import get_correct_url


class ArticleHtmlParser:
    def __init__(self, response: Response, project: Project):
        self.page = response
        self.project = project
        self.title: str | None = None
        self.img_url: str | None = None
        self.body: str | None = None

    @staticmethod
    async def parse_data(html: str, element: dict) -> ResultSet:
        # TODO: Add documentation
        soup = bs(html, "html.parser")
        parse_result = soup.find_all(
            element["selector"],
            attrs=element["attr"],
        )
        # Decode all CloudFlare encoded mails
        for parse_item in parse_result:
            cloudflare_emails = parse_item.find_all(class_="__cf_email__")
            if cloudflare_emails:
                for encoded_mail in cloudflare_emails:
                    encoded_value = encoded_mail.get("data-cfemail")
                    fixed_result = await cloudflare_decode_email(encoded_value)
                    encoded_mail.string = fixed_result

        return parse_result

    async def get_title(self):
        soup = bs(self.page.text, "html.parser")
        self.title = soup.title.string if soup.title else None

    async def get_img(self):
        images: ResultSet = await self.parse_data(
            self.page.text, self.project.parse_article_img_element
        )
        if images:
            image_link = await get_correct_url(
                self.project.url, images[0].find("img").get("src")
            )
            self.img_url = image_link

    async def get_body(self):
        body: ResultSet = await self.parse_data(
            self.page.text, self.project.parse_article_body_element
        )
        body_string = " ".join([e.text for e in body])

        normalized_body = re.sub(r"\xa0", "", body_string)
        normalized_body = re.sub(r"\n\n+", "\n\n", normalized_body).strip()
        self.body = normalized_body

    @property
    async def get_article(self) -> Article:
        await self.get_title()
        await self.get_img()
        await self.get_body()

        return Article(
            url=str(self.page.url),
            title=self.title or "",
            img_url=self.img_url or "",
            body=self.body or "",
            project_id=self.project.id,
        )


class ParserController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def collect_urls_by_html(
        self, client: AsyncClient, object: Project
    ) -> list[str]:
        # TODO: Add documentation
        aggregate_url = object.url
        urls = []
        response = await client.get(aggregate_url)
        results = await ArticleHtmlParser.parse_data(
            response.text, object.parse_article_url_element
        )

        for result in results:
            url = await get_correct_url(object.url, result["href"])
            urls.append(url)

        return urls

    async def collect_by_html(self, object: Project) -> None:
        # TODO: Add documentation
        client = await get_request_client()

        try:
            # Collect all urls from aggregate page
            urls: list[str] = await self.collect_urls_by_html(client, object)
            # TODO: Add info about collecting urls
            urls_in_db = await self.session.exec(
                select(Article.url).where(Article.url.in_(urls))
            )
            urls_in_db_result = urls_in_db.unique().all()

            # Get only unique Urls
            urls = list(set(urls) - set(urls_in_db_result))

            for url in urls:
                # Getting elements of article from each url
                response = await client.get(url)
                article = await ArticleHtmlParser(response, object).get_article

                self.session.add(article)
                await self.session.commit()
                await self.session.refresh(article)
        finally:
            await client.aclose()

        # TODO: Add implementation of sending notification about added articles
        # TODO: SAVE to DB log
        print(f"DONE! Added - {len(urls)}")

    async def collect_data(self, object_id: int) -> Project:
        # TODO: Add documentation
        db_object = await self.session.get(Project, object_id)

        if not db_object:
            raise HTTPException(status_code=404, detail="Project not found")

        match db_object.parse_type:
            # TODO: Add logger
            case "html":
                await self.collect_by_html(db_object)
            case _:
                raise HTTPException(
                    status_code=status.HTTP_501_NOT_IMPLEMENTED,
                    detail="This parse type is not implemented yet.",
                )
        # TODO: Add logger
        print(f"Task done - for project id: {object_id}")
        return db_object
