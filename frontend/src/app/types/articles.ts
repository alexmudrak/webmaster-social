export interface CollectArticlesButtonProps {
  project_name: string
  project_id?: number
}
export interface NetworkStatus {
  id?: number | null
  name: string
  status: 'DONE' | 'ERROR' | 'PENDING'
  status_text: string
  url?: string
}
export interface NetworkStatusIconProps {
  article_id: number
  status: NetworkStatus
  name: string
}

export interface Article {
  id: number
  created: string
  project_name: string
  title: string
  network_statuses: NetworkStatus[]
}

export interface ArticlePageResponse {
  url: string
  title: string
  img_url: string
  body: string
  project_id: number
  id: number
  created: string
  project_name: string
  network_statuses: NetworkStatus[]
}
