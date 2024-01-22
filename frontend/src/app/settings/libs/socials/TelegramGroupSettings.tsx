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

export default function TelegramGroupSettings({
  title,
  data,
  handlerSettingUpdate,
  handlerCloseModal
}: SocialAppProps) {
  // TODO: Change app_id to client_id
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
          label='Group ID'
          id='group-id'
          name='group_id'
          value={setting.settings.group_id}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          multiline
          maxRows={6}
          label='Access Token'
          id='access-token'
          name='access_token'
          value={setting.settings.access_token}
          onChange={handleInputChange}
        />

        <Button variant='contained' onClick={handleSave}>
          Save
        </Button>
      </Stack>
    </>
  )
}
