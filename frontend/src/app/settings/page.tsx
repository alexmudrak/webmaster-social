'use client'

import AddCircleIcon from '@mui/icons-material/AddCircle'
import { Box, Divider, IconButton, Tab, Tabs, Typography } from '@mui/material'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import TabPanel from '../components/TabPanel'
import { socialNetworksList } from '../constants/SocialNetworks'
import { Project } from '../types/project'
import {
  GroupedSettings,
  Setting,
  SocialAppTitleKey
} from '../types/social_network_settings'
import { apiRequest } from '../utils/apiRequest'
import ProjectAppModal from './components/projects/ProjectAppModal'
import ProjectAppSettings from './components/projects/ProjectAppSettings'
import SocialAppSettings from './components/social_networks/SocialAppSettings'

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`
  }
}

export default function Settings() {
  // TODO: Add list of available social networks
  const [value, setValue] = React.useState(0)

  const [projectsData, setProjectsData] = React.useState<Project[]>([])
  const [socialNetworksData, setSocialNetworksData] =
    React.useState<GroupedSettings>({})

  const isMounted = React.useRef(false)
  React.useEffect(() => {
    const fetchProjects = async () => {
      const endpoint = 'projects/'
      const response = await apiRequest(endpoint, { method: 'GET' })
      setProjectsData(response)
      return response
    }

    const fetchSocialNetworks = async () => {
      const endpoint = 'settings/'
      const response = await apiRequest(endpoint, { method: 'GET' })

      return response.reduce((acc: GroupedSettings, setting: Setting) => {
        const { name } = setting
        if (!acc[name]) {
          acc[name] = []
        }
        acc[name].push(setting)
        return acc
      }, {})
    }

    const updateSocialNetworksData = (
      projects: Project[],
      socialNetworks: GroupedSettings
    ) => {
      const updatedSocialNetworksData = { ...socialNetworks }

      socialNetworksList.forEach((network) => {
        if (!updatedSocialNetworksData[network]) {
          updatedSocialNetworksData[network] = []
        }

        projects.forEach((project) => {
          const projectExists = updatedSocialNetworksData[network].some(
            (setting) => setting.project_name === project.name
          )

          if (!projectExists) {
            const defaultSetting: Setting = {
              name: network,
              settings: {},
              project_id: project.id,
              active: false,
              id: null,
              project_name: project.name
            }
            updatedSocialNetworksData[network].push(defaultSetting)
          }
        })
      })
      setSocialNetworksData(updatedSocialNetworksData)
    }

    if (!isMounted.current) {
      isMounted.current = true
      Promise.all([fetchProjects(), fetchSocialNetworks()]).then(
        ([projects, socialNetworks]) => {
          updateSocialNetworksData(projects, socialNetworks)
        }
      )
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
          <Tab label='Social networks' {...a11yProps(1)} />
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
          {Object.entries(socialNetworksData).map(([key, settingsList]) => {
            const title = key as SocialAppTitleKey
            return (
              <SocialAppSettings
                key={title}
                title={title}
                data={settingsList}
              />
            )
          })}
        </Grid>
      </TabPanel>
    </>
  )
}
