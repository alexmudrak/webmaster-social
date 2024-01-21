import Button from '@mui/material/Button'
import Divider from '@mui/material/Divider'
import FormControlLabel from '@mui/material/FormControlLabel'
import Stack from '@mui/material/Stack'
import Switch from '@mui/material/Switch'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import { SocialAppProps } from '../../../types/social_network_settings'

export default function InstagramSettings({
  title,
  data,
  handlerSettingUpdate,
  handlerCloseModal
}: SocialAppProps) {
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
          label='Username'
          id='username'
          name='username'
          value={setting.settings.username}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='Password'
          id='password'
          name='password'
          value={setting.settings.password}
          onChange={handleInputChange}
          type='password'
        />

        <TextField
          fullWidth
          label='MID'
          id='mid'
          name='cookies.mid'
          value={setting.settings.cookies?.mid}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='CSRF Token'
          id='csrftoken'
          name='cookies.csrftoken'
          value={setting.settings.cookies?.csrftoken}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='DS User ID'
          id='ds-user-id'
          name='cookies.ds_user_id'
          value={setting.settings.cookies?.ds_user_id}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='Session ID'
          id='sessionid'
          name='cookies.sessionid'
          value={setting.settings.cookies?.sessionid}
          onChange={handleInputChange}
        />

        <Button variant='contained' onClick={handleSave}>
          Save
        </Button>
      </Stack>
    </>
  )
}
