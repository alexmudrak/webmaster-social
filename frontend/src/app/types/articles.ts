export interface CollectArticlesButtonProps {
  project_name: string;
  project_id: number;
}
export interface NetworkStatusIconProps {
  article_id: number
  status: {
    id: number
    name: string
    status: 'DONE' | 'ERROR' | 'PENDING'
    status_text: string
    url: string
  }
  name: string
}
