export interface Project {
  name: string;
  url: string;
  active: boolean;
  parse_type: string;
  parse_last_article_count: number;
  parse_article_url_element: {
    selector: string;
    attrs: string;
  };
  parse_article_img_element: {
    selector: string;
    attrs: string;
  };
  parse_article_body_element: {
    selector: string;
    attrs: string[];
  };
  id: number;
}

export interface ProjectModalProps {
  open: boolean
  handleClose: () => void
  data?: Project
}
