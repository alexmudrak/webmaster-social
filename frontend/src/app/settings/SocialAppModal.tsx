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
import { Setting, SocialAppModalProps } from '../types/social_network_settings'
import SocialOne from './libs/socials/socialAppOne'

export default function SocialAppModal({
  title,
  open,
  handleClose,
  data
}: SocialAppModalProps) {
  const [valueTab, setValueTab] = React.useState(0)
  const handleChangeTab = (_: React.SyntheticEvent, newValue: number) => {
    setValueTab(newValue)
  }

  const renderSocialComponent = (title: string, setting: Setting) => {
    switch (title) {
      case 'instagram':
        return (
          <SocialOne
            title={title}
            data={setting}
          />
        )
      default:
        return null
    }
  }

  if (!data) {
    return null
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
            {data.map((setting, index) => (
              <Tab
                key={setting.id}
                label={setting.project_name}
                {...a11yProps(index)}
              />
            ))}
          </Tabs>
        </Box>

        <Divider sx={{ my: 1.5 }} />

        {data.map((setting, index) => (
          <TabPanel key={setting.id} value={valueTab} index={index}>
            {renderSocialComponent(title, setting)}
          </TabPanel>
        ))}
      </Box>
    </Modal>
  )
}
