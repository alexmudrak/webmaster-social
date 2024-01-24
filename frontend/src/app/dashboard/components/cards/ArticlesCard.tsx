import LibraryBooksIcon from '@mui/icons-material/LibraryBooks'
import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Tooltip from '@mui/material/Tooltip'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import { ArticlesCardProps } from '../../../types/dashboard'

export default function ArticlesCard({
  total,
  published,
  with_error
}: ArticlesCardProps) {
  return (
    <Grid xs={4}>
      <Card sx={{ display: 'flex', }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
          <CardContent sx={{ flex: '1 0 auto' }}>
            <Typography color='text.secondary' gutterBottom>
              Articles
            </Typography>
            <Typography variant='h5' component='div'>
              <Tooltip title='Total articles' arrow>
                <span style={{ color: 'black' }}>{total}</span>
              </Tooltip>
              {' / '}
              <Tooltip title='Published articles' arrow>
                <span style={{ color: 'green' }}>{published}</span>
              </Tooltip>
              {' / '}
              <Tooltip title='Articles with errors' arrow>
                <span style={{ color: 'red' }}>{with_error}</span>
              </Tooltip>
            </Typography>
          </CardContent>
        </Box>
        <CardContent>
          <LibraryBooksIcon sx={{ fontSize: 50 }} />
        </CardContent>
      </Card>
    </Grid>
  )
}
