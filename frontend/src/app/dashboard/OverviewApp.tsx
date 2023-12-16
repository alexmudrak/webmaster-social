import InsertEmoticonIcon from '@mui/icons-material/InsertEmoticon'
import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

export default function OverviewApp() {
  return (
    <Grid xs={4}>
      <Card sx={{ display: 'flex' }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
          <CardContent sx={{ flex: '1 0 auto' }}>
            <Typography color='text.secondary' gutterBottom>
              title card
            </Typography>
            <Typography variant='h5' component='div'>
              999
            </Typography>
          </CardContent>
        </Box>
        <CardContent>
          <InsertEmoticonIcon sx={{ fontSize: 50 }} />
        </CardContent>
      </Card>
    </Grid>
  )
}
