import {
  Button,
  Divider,
  FormControlLabel,
  Stack,
  Switch,
  TextField,
  Typography
} from '@mui/material'
import * as React from 'react'

import { SocialAppProps } from '../../../types/social_network_settings'

export default function TwitterSettings({
  title,
  data,
  handlerSettingUpdate,
  handlerCloseModal
}: SocialAppProps) {
  // TODO: Change redirect_uri to redirect_url
  const [setting, updateSetting] = React.useState(data)
  const switchLabel = setting?.active ? 'On' : 'Off'

  const handleActiveChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      updateSetting((prevData) => ({
        ...prevData,
        active: event.target.checked
      }))
    },
    []
  )

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    const [field, subField] = name.split('.')

    if (subField) {
      updateSetting((prevData) => ({
        ...prevData,
        settings: {
          ...prevData.settings,
          cookies: {
            ...prevData.settings.cookies,
            [subField]: value
          }
        }
      }))
    } else {
      updateSetting((prevData) => ({
        ...prevData,
        settings: {
          ...prevData.settings,
          [field]: value
        }
      }))
    }
  }

  const handleSave = () => {
    handlerSettingUpdate(setting.id, setting)
    handlerCloseModal()
  }

  return (
    <>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <Typography variant='h5' id='modal-project-title'>
          {`${title} settings for '${setting.project_name}'`}
        </Typography>
        <FormControlLabel
          control={
            <Switch checked={setting.active} onChange={handleActiveChange} />
          }
          label={switchLabel}
        />
      </div>

      <Divider sx={{ marginY: 2 }} />

      <Stack
        sx={{
          width: '100%'
        }}
        spacing={2}
      >
        <TextField
          fullWidth
          label='Client ID'
          id='client-id'
          name='client_id'
          value={setting.settings.client_id}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='Client Secret'
          id='client-secret'
          name='client_secret'
          value={setting.settings.client_secret}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='APP Redirect URL'
          id='redirect-uri'
          name='redirect_uri'
          value={setting.settings.redirect_uri}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          multiline
          maxRows={6}
          label='Refresh Token'
          id='refresh-token'
          name='refresh_token'
          value={setting.settings.refresh_token}
          onChange={handleInputChange}
        />

        <Button variant='contained' onClick={handleSave}>
          Save
        </Button>
      </Stack>
    </>
  )
}
