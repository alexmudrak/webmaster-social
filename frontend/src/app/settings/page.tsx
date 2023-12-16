'use client'
import AddCircleIcon from '@mui/icons-material/AddCircle'
import Box from '@mui/material/Box'
import IconButton from '@mui/material/IconButton'
import Tab from '@mui/material/Tab'
import Tabs from '@mui/material/Tabs'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import TabPanel from '../components/TabPanel'
import ProjectAppModal from './ProjectAppModal'
import ProjectAppSettings from './ProjectAppSettings'
import SocialAppSettings from './SocialAppSettings'

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`
  }
}

export default function Page() {
  const [value, setValue] = React.useState(0)

  const handleChange = (_: React.SyntheticEvent, newValue: number) => {
    setValue(newValue)
  }

  const [openProjectModal, setOpenProjectModal] = React.useState(false)
  const handleAddProject = () => {
    setOpenProjectModal(true)
  }
  const handleProjectModalClose = () => {
    setOpenProjectModal(false)
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
      <TabPanel value={value} index={0}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <Typography
            variant='h4'
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            Active projects
          </Typography>
          <IconButton
            onClick={handleAddProject}
            color='primary'
            aria-label='add project'
          >
            <AddCircleIcon fontSize='large' />
          </IconButton>
        </div>
        <Grid container spacing={2}>
          <ProjectAppSettings title='Mock project 1' />
          <ProjectAppSettings title='Mock project 2' />
          <ProjectAppSettings title='Mock project 3' />
        </Grid>

        <ProjectAppModal
          open={openProjectModal}
          handleClose={handleProjectModalClose}
        />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <Typography
          variant='h4'
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          Available networks
        </Typography>
        <Grid container spacing={2}>
          <SocialAppSettings title='Mock social network 1' />
          <SocialAppSettings title='Mock social network 2' />
          <SocialAppSettings title='Mock social network 3' />
          <SocialAppSettings title='Mock social network 4' />
        </Grid>
      </TabPanel>
    </>
  )
}
