'use client'
import Box from '@mui/material/Box'
import Tab from '@mui/material/Tab'
import Tabs from '@mui/material/Tabs'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import SocialAppSettings from './SocialAppSettings'

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`
  }
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props

  return (
    <div
      role='tabpanel'
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  )
}

export default function Page() {
  const [value, setValue] = React.useState(0)

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue)
  }
  return (
    <>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label='basic tabs example'
        >
          <Tab label='Projects' {...a11yProps(0)} />
          <Tab label='Publishing networks' {...a11yProps(1)} />
        </Tabs>
      </Box>
      <CustomTabPanel value={value} index={1}>
        <Typography variant='h4'>Publishing networks</Typography>
        <Grid container spacing={2}>
          <SocialAppSettings title='Mock social network 1' />
          <SocialAppSettings title='Mock social network 2' />
          <SocialAppSettings title='Mock social network 3' />
          <SocialAppSettings title='Mock social network 4' />
        </Grid>
      </CustomTabPanel>
    </>
  )
}
