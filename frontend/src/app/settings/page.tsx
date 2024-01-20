'use client'
import AddCircleIcon from '@mui/icons-material/AddCircle'
import { Divider } from '@mui/material'
import Box from '@mui/material/Box'
import IconButton from '@mui/material/IconButton'
import Tab from '@mui/material/Tab'
import Tabs from '@mui/material/Tabs'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import TabPanel from '../components/TabPanel'
import { Project } from '../types/project'
import ProjectAppModal from './ProjectAppModal'
import ProjectAppSettings from './ProjectAppSettings'
import SocialAppSettings from './SocialAppSettings'

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`
  }
}

export default function Settings() {
  const [value, setValue] = React.useState(0)

  const [projectsData, setProjectsData] = React.useState<Project[]>([])
  const [socialNetworksData, setSocialNetworksData] = React.useState([])

  React.useEffect(() => {
    const fetchProjects = async () => {
      const response = await fetch('http://localhost:8000/api/v1/projects/')
      const data: Project[] = await response.json()
      setProjectsData(data)
    }

    const fetchSocialNetworks = async () => {
      const response = await fetch('http://localhost:8000/api/v1/settings/')
      const data = await response.json()
      setSocialNetworksData(data)
    }

    if (value === 0) {
      fetchProjects()
    } else if (value === 1) {
      fetchSocialNetworks()
    }
  }, [value])

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

  // TODO: Add updating Project item after Create/Update/Delete
  return (
    <>
      <Box>
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label='basic tabs example'
        >
          <Tab label='Projects' {...a11yProps(0)} />
          <Tab label='Publishing networks' {...a11yProps(1)} />
        </Tabs>
      </Box>

      <Divider sx={{ my: 1.5 }} />

      <TabPanel value={value} index={0}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <Typography variant='h4'>Active projects</Typography>
          <IconButton
            onClick={handleAddProject}
            color='primary'
            aria-label='add project'
          >
            <AddCircleIcon fontSize='large' />
          </IconButton>
        </div>

        <Divider sx={{ my: 1.5 }} />

        <Grid container spacing={2}>
          {projectsData.map((project) => (
            <ProjectAppSettings key={project.id} data={project} />
          ))}
        </Grid>

        <ProjectAppModal
          open={openProjectModal}
          handleClose={handleProjectModalClose}
        />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <Typography variant='h4'>Available networks</Typography>

        <Divider sx={{ my: 1.5 }} />

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
