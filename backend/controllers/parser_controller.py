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
    def __init__(self, response: Response, project: Project) -> None:
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
        images = await self.parse_data(
            self.page.text, self.project.parse_article_img_element
        )
        if images:
            image_link = await get_correct_url(
                self.project.url, images[0].find("img").get("src")
            )
            self.img_url = image_link

    async def get_body(self):
        body = await self.parse_data(
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
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def collect_urls_by_html(
        self, client: AsyncClient, project: Project
    ) -> list[str]:
        # TODO: Add documentation
        aggregate_url = project.url
        response = await client.get(aggregate_url)
        results = await ArticleHtmlParser.parse_data(
            response.text, project.parse_article_url_element
        )

        urls = [
            await get_correct_url(project.url, result["href"])
            for result in results
        ]

        return urls

    async def get_unique_urls(
        self, client: AsyncClient, project: Project
    ) -> list[str]:
        # TODO: Add documentation
        # Collect all urls from aggregate page
        urls = await self.collect_urls_by_html(client, project)
        # TODO: Add info about collecting urls
        urls_in_db = await self.session.exec(
            select(Article.url).where(Article.url.in_(urls))
        )
        urls_in_db_result = urls_in_db.unique().all()

        # Return only unique Urls
        return list(set(urls) - set(urls_in_db_result))

    async def add_articles_to_db(
        # TODO: Add documentation
        self,
        client: AsyncClient,
        project: Project,
        urls: list[str],
    ) -> None:
        for url in urls:
            # Getting elements of article from each url
            response = await client.get(url)
            article = await ArticleHtmlParser(response, project).get_article

            self.session.add(article)
            await self.session.commit()
            await self.session.refresh(article)

        # TODO: Add implementation of sending notification about added articles
        # TODO: SAVE to DB log
        print(f"DONE! Added - {len(urls)}")

    async def collect_by_html(self, project: Project) -> None:
        # TODO: Add documentation
        client = await get_request_client()
        try:
            urls_to_add = await self.get_unique_urls(client, project)
            await self.add_articles_to_db(client, project, urls_to_add)
        finally:
            await client.aclose()

    async def collect_data(self, project_id: int) -> Project:
        # TODO: Add documentation
        db_project = await self.session.get(Project, project_id)

        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")

        # TODO: Add logger
        if db_project.parse_type == "html":
            await self.collect_by_html(db_project)
        else:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="This parse type is not implemented yet.",
            )
        # TODO: Add logger
        print(f"Task done - for project id: {project_id}")
        return db_project
