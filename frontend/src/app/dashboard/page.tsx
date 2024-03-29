'use client'
import { Divider } from '@mui/material'
import Box from '@mui/material/Box'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import { DashboardCardData, DashboardStatusesData } from '../types/dashboard'
import { apiRequest } from '../utils/apiRequest'
import ArticlesCard from './components/cards/ArticlesCard'
import NetworksCard from './components/cards/NetworksCard'
import ProjectsCard from './components/cards/ProjectsCard'
import RunStatusApp from './status/RunStatusApp'

export default function Page() {
  const [expanded, setExpanded] = React.useState<string | false>(false)
  const [cardData, setCardData] = React.useState<DashboardCardData | null>(
    null
  )

  const [statusesData, setStatusesData] = React.useState<
    DashboardStatusesData[] | null
  >(null)

  const isMounted = React.useRef(false)

  React.useEffect(() => {
    const fetchCardData = async () => {
      const method = 'GET'
      const endpoint = `dashboards/cards`

      const response = await apiRequest(endpoint, {
        method: method
      })
      setCardData(response)
    }

    const fetchStatusesData = async () => {
      const method = 'GET'
      const endpoint = `dashboards/statuses`

      const response = await apiRequest(endpoint, {
        method: method
      })
      setStatusesData(response)
    }

    if (!isMounted.current) {
      isMounted.current = true
      fetchCardData()
      fetchStatusesData()
    }
  }, [])

  const handleChange =
    (panel: string) => (_: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false)
    }

  return (
    <Container maxWidth='xl' sx={{ marginTop: 2 }}>
      <Typography variant='h4'>Overview</Typography>

      <Divider sx={{ my: 1.5 }} />

      <Box sx={{ margin: 2 }}>
        <Grid container spacing={2}>
          <ArticlesCard
            total={cardData?.articles.total}
            published={cardData?.articles.published}
            with_error={cardData?.articles.with_error}
          />
          <ProjectsCard total={cardData?.projects.total} />
          <NetworksCard total={cardData?.networks.total} />
        </Grid>
      </Box>

      <Typography variant='h4'>Last 5 status</Typography>

      <Divider sx={{ my: 1.5 }} />

      <Box sx={{ margin: 2 }}>
        {statusesData?.map((status, index) => (
          <RunStatusApp
            key={status.article_id}
            panel={`panel_${index}`}
            expanded={expanded === `panel_${index}`}
            handleChange={handleChange}
            statusData={status}
          />
        ))}
      </Box>
    </Container>
  )
}
