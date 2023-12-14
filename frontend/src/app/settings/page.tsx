import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import SocialAppSettings from './socialAppSettings'

export default function Page() {
  return (
    <>
      <Typography variant='h5'>Publishing networks</Typography>
      <Grid container spacing={2}>
        <SocialAppSettings title='Mock social network 1' />
        <SocialAppSettings title='Mock social network 2' />
        <SocialAppSettings title='Mock social network 3' />
        <SocialAppSettings title='Mock social network 4' />
      </Grid>
    </>
  )
}
