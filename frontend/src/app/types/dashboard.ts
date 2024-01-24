export interface DashboardCardData {
  articles: {
    total: number;
    published: number;
    with_error: number;
  };
  projects: {
    total: number;
  };
  networks: {
    total: number;
  };
}

export interface ArticlesCardProps {
  total?: number;
  published?: number;
  with_error?: number;
}

export interface CommonCardProps {
  total?: number;
}
