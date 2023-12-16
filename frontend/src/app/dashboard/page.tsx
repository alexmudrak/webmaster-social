'use client'
import Box from '@mui/material/Box'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import OverviewApp from './OverviewApp'
import RunStatusApp from './RunStatusApp'

export default function Page() {
  const [expanded, setExpanded] = React.useState<string | false>(false)

  const handleChange =
    (panel: string) => (_: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false)
    }
  return (
    <Container maxWidth='xl' sx={{ marginTop: 2 }}>
      <Typography
        sx={{ borderBottom: 1, borderColor: 'divider' }}
        variant='h4'
      >
        Overview
      </Typography>
      <Box sx={{ margin: 2 }}>
        <Grid container spacing={2}>
          <OverviewApp />
          <OverviewApp />
          <OverviewApp />
        </Grid>
      </Box>

      <Typography
        sx={{ borderBottom: 1, borderColor: 'divider' }}
        variant='h4'
      >
        Run status
      </Typography>
      <Box sx={{ margin: 2 }}>
        <RunStatusApp
          panel='panel_1'
          expanded={expanded}
          handleChange={handleChange}
        />
        <RunStatusApp
          panel='panel_2'
          expanded={expanded}
          handleChange={handleChange}
        />
        <RunStatusApp
          panel='panel_3'
          expanded={expanded}
          handleChange={handleChange}
        />
      </Box>
    </Container>
  )
}
