'use client'
import { Divider } from '@mui/material'
import Box from '@mui/material/Box'
import Modal from '@mui/material/Modal'
import Tab from '@mui/material/Tab'
import Tabs from '@mui/material/Tabs'
import * as React from 'react'

import a11yProps from '../components/a11Props'
import TabPanel from '../components/TabPanel'
import { modalStyle } from '../styles/modalStyle'
import SocialOne from './libs/socials/socialAppOne'

interface SocialAppModalProps {
  title: string
  open: boolean
  handleClose: () => void
}

export default function SocialAppModal({
  title,
  open,
  handleClose
}: SocialAppModalProps) {
  const [valueTab, setValueTab] = React.useState(0)
  const handleChangeTab = (_: React.SyntheticEvent, newValue: number) => {
    setValueTab(newValue)
  }
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby='modal-social-title'
      aria-describedby='modal-social-description'
    >
      <Box sx={modalStyle}>
        <Box>
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

        <Divider sx={{ my: 1.5 }} />

        <TabPanel value={valueTab} index={0}>
          <SocialOne title={`General settings for '${title}'`} />
        </TabPanel>
        <TabPanel value={valueTab} index={1}>
          <SocialOne title={`{project_1} settings for '${title}'`} />
        </TabPanel>
        <TabPanel value={valueTab} index={2}>
          <SocialOne title={`{project_2} settings for '${title}'`} />
        </TabPanel>
        <TabPanel value={valueTab} index={3}>
          <SocialOne title={`{project_3} settings for '${title}'`} />
        </TabPanel>
      </Box>
    </Modal>
  )
}
