import * as React from 'react'

export interface DashboardCardData {
  articles: {
    total: number
    published: number
    with_error: number
  }
  projects: {
    total: number
  }
  networks: {
    total: number
  }
}

export interface ArticlesCardProps {
  total?: number
  published?: number
  with_error?: number
}

export interface CommonCardProps {
  total?: number
}

export interface DashboardNetworkStatusesData {
  id: number
  date: string
  name: string
  status: string
  status_text: string | null
}

export interface DashboardStatusesData {
  date: string
  project_name: string
  article_id: number
  article_title: string
  network_statuses: DashboardNetworkStatusesData[]
}

export interface RunStatusAppProps {
  panel: string
  expanded: boolean
  handleChange: (
    _panel: string
  ) => (_event: React.SyntheticEvent, _isExpanded: boolean) => void
  statusData: DashboardStatusesData
}

export interface RunStatusAppDetailProps {
  networkStatuses: DashboardNetworkStatusesData[]
}
