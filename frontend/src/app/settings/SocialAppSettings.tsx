'use client'
import SettingsIcon from '@mui/icons-material/Settings'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardHeader from '@mui/material/CardHeader'
import FormControlLabel from '@mui/material/FormControlLabel'
import IconButton from '@mui/material/IconButton'
import Switch from '@mui/material/Switch'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import {
  Setting,
  SocialAppSettingsProps
} from '../types/social_network_settings'
import SocialAppModal from './SocialAppModal'

export default function SocialAppSettings({
  title,
  data
}: SocialAppSettingsProps) {
  const [settings, setSettings] = React.useState(data)
  const [openSocialAppModal, setOpenSocialAppModal] = React.useState(false)

  const handleSocialAppModalOpen = () => setOpenSocialAppModal(true)
  const handleSocialAppModalClose = () => setOpenSocialAppModal(false)

  const handlerSettingUpdate = async (id: number, setting: Setting) => {
    setSettings((prevSettings) =>
      prevSettings.map((item) =>
        item.id === id ? { ...item, ...setting } : item
      )
    )

    await sendUpdateSetting(id, setting)
  }

  const handleSettingActiveChange =
    (id: number) => async (event: React.ChangeEvent<HTMLInputElement>) => {
      const newActiveState = event.target.checked
      const updatedItem = settings.find((item) => item.id === id)
      if (!updatedItem) {
        return
      }

      const updatedSettings = {
        ...updatedItem,
        active: newActiveState
      }

      handlerSettingUpdate(id, updatedSettings)
    }

  const sendUpdateSetting = async (id: number, updatedData: Setting) => {
    const url =
      id === null
        ? 'http://localhost:8000/api/v1/settings/'
        : `http://localhost:8000/api/v1/settings/${id}`
    const method = id === null ? 'POST' : 'PATCH'

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to update setting:', error)
    }
  }

  return (
    <Grid xs={12} sm={6} lg={6}>
      <Card>
        <CardHeader
          action={
            <IconButton
              aria-label='settings'
              onClick={handleSocialAppModalOpen}
            >
              <SettingsIcon />
            </IconButton>
          }
          title={title}
          subheader='{last_publish_date}'
        />
        <CardContent>
          {settings.map((setting, index) => (
            <div key={setting.id !== null ? setting.id : `setting-${index}`}>
              <FormControlLabel
                control={
                  <Switch
                    checked={setting.active}
                    onChange={handleSettingActiveChange(setting.id)}
                    color='primary'
                  />
                }
                label={setting.project_name}
              />
            </div>
          ))}
        </CardContent>
        <SocialAppModal
          title={title}
          data={settings}
          open={openSocialAppModal}
          handleClose={handleSocialAppModalClose}
          handlerSettingUpdate={handlerSettingUpdate}
        />
      </Card>
    </Grid>
  )
}
