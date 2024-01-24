import LanguageIcon from '@mui/icons-material/Language'
import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Tooltip from '@mui/material/Tooltip'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import { CommonCardProps } from '../../../types/dashboard'

export default function NetworksCard({ total }: CommonCardProps) {
  return (
    <Grid xs={4}>
      <Card sx={{ display: 'flex' }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
          <CardContent sx={{ flex: '1 0 auto' }}>
            <Typography color='text.secondary' gutterBottom>
              Networks
            </Typography>
            <Typography variant='h5' component='div'>
              <Tooltip title='Total networks' arrow>
                <span style={{ color: 'black' }}>{total}</span>
              </Tooltip>
            </Typography>
          </CardContent>
        </Box>
        <CardContent>
          <LanguageIcon sx={{ fontSize: 50 }} />
        </CardContent>
      </Card>
    </Grid>
  )
}
