'use client'
import SettingsIcon from '@mui/icons-material/Settings'
import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardHeader from '@mui/material/CardHeader'
import FormControlLabel from '@mui/material/FormControlLabel'
import IconButton from '@mui/material/IconButton'
import Modal from '@mui/material/Modal'
import Switch from '@mui/material/Switch'
import Tab from '@mui/material/Tab'
import Tabs from '@mui/material/Tabs'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import SocialOne from './libs/socials/social_one'

interface SocialAppSettingsProps {
  title: string
}

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '75%',
  bgcolor: 'background.paper',
  borderRadius: 1,
  boxShadow: 24,
  p: 4
}
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

export default function SocialAppSettings({ title }: SocialAppSettingsProps) {
  const switchData: { label: string; id: string }[] = [
    { label: '{project_name_1}', id: 'project1' },
    { label: '{project_name_2}', id: 'project2' },
    { label: '{project_name_3}', id: 'project3' }
  ]

  const [switchStates, setSwitchStates] = React.useState<{
    [key: string]: boolean
  }>(
    switchData.reduce((acc, switchItem) => {
      acc[switchItem.id] = false
      return acc
    }, {})
  )

  const handleChange =
    (id: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setSwitchStates((prevState) => ({
        ...prevState,
        [id]: event.target.checked
      }))
    }

  const [openModal, setOpenModal] = React.useState(false)
  const handleModalOpen = () => setOpenModal(true)
  const handleModalClose = () => setOpenModal(false)
  const [valueTab, setValueTab] = React.useState(0)
  const handleChangeTab = (event: React.SyntheticEvent, newValue: number) => {
    setValueTab(newValue)
  }
  return (
    <Grid xs={12} sm={6} lg={3}>
      <Modal
        open={openModal}
        onClose={handleModalClose}
        aria-labelledby='modal-modal-title'
        aria-describedby='modal-modal-description'
      >
        <Box sx={style}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs
              value={valueTab}
              onChange={handleChangeTab}
              aria-label='basic tabs example'
            >
              <Tab label='General' {...a11yProps(0)} />
              <Tab label='Project 1' {...a11yProps(1)} />
              <Tab label='Project 2' {...a11yProps(2)} />
              <Tab label='Project 3' {...a11yProps(3)} />
            </Tabs>
          </Box>

          <CustomTabPanel value={valueTab} index={0}>
            <Typography variant='h5' sx={{ marginBottom: 2 }}>
              {'General settings for { network }'}
            </Typography>
            <SocialOne />
          </CustomTabPanel>
          <CustomTabPanel value={valueTab} index={1}>
            <Typography variant='h5' sx={{ marginBottom: 2 }}>
              {'{project 1} settings for { network }'}
            </Typography>
            <SocialOne />
          </CustomTabPanel>
          <CustomTabPanel value={valueTab} index={2}>
            <Typography variant='h5' sx={{ marginBottom: 2 }}>
              {'{project 2} settings for { network }'}
            </Typography>
            <SocialOne />
          </CustomTabPanel>
          <CustomTabPanel value={valueTab} index={3}>
            <Typography variant='h5' sx={{ marginBottom: 2 }}>
              {'{project 3} settings for { network }'}
            </Typography>
            <SocialOne />
          </CustomTabPanel>
        </Box>
      </Modal>
      <Card>
        <CardHeader
          action={
            <IconButton aria-label='settings' onClick={handleModalOpen}>
              <SettingsIcon />
            </IconButton>
          }
          title={title}
          subheader='{last_publish_date}'
        />
        <CardContent>
          {switchData.map((switchItem) => (
            <div key={switchItem.id}>
              <FormControlLabel
                control={
                  <Switch
                    checked={switchStates[switchItem.id]}
                    onChange={handleChange(switchItem.id)}
                    color='primary'
                    value={switchItem.id}
                  />
                }
                label={switchItem.label}
              />
            </div>
          ))}
        </CardContent>
      </Card>
    </Grid>
  )
}
