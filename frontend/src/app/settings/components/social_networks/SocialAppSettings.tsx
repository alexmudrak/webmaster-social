import SettingsIcon from '@mui/icons-material/Settings'
import {
  Card,
  CardContent,
  CardHeader,
  FormControlLabel,
  IconButton,
  Switch
} from '@mui/material'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import {
  Setting,
  SocialAppSettingsProps
} from '../../../types/social_network_settings'
import { apiRequest } from '../../../utils/apiRequest'
import SocialAppModal from './SocialAppModal'

export default function SocialAppSettings({
  title,
  data
}: SocialAppSettingsProps) {
  const [settings, setSettings] = React.useState(data)
  const [openSocialAppModal, setOpenSocialAppModal] = React.useState(false)

  const handleSocialAppModalOpen = () => setOpenSocialAppModal(true)
  const handleSocialAppModalClose = () => setOpenSocialAppModal(false)

  const handlerSettingUpdate = async (
    id: number | null,
    setting: Setting | null
  ) => {
    setSettings((prevSettings) =>
      prevSettings.map((item) =>
        item.id === id ? { ...item, ...setting } : item
      )
    )

    await sendUpdateSetting(id, setting)
  }

  const handleSettingActiveChange =
    (id: number | null) =>
    async (event: React.ChangeEvent<HTMLInputElement>) => {
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

  const sendUpdateSetting = async (
    id: number | null,
    updatedData: Setting | null
  ) => {
    const method = id ? 'PATCH' : 'POST'
    const endpoint = id ? `settings/${id}` : 'settings/'

    await apiRequest(endpoint, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updatedData)
    })
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
