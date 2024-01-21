import Button from '@mui/material/Button'
import Divider from '@mui/material/Divider'
import FormControlLabel from '@mui/material/FormControlLabel'
import Stack from '@mui/material/Stack'
import Switch from '@mui/material/Switch'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import { Setting } from '../../../types/social_network_settings'

interface SocialOneProps {
  title: string
  data: Setting
}

export default function SocialOne({ title, data }: SocialOneProps) {
  // TODO: Move data change handler from AppSetting
  const [setting, changeSetting] = React.useState(data)
  const switchLabel = setting?.active ? 'On' : 'Off'

  const handleActiveChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      console.log(event)
      changeSetting((prevData) => ({
        ...prevData,
        active: event.target.checked
      }))
    },
    []
  )

  // TODO: Move data change handler from AppSetting
  const handleSave = async () => {
    const response = await fetch(
      `http://localhost:8000/api/v1/settings/${data?.id}`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(setting)
      }
    )

    if (!response.ok) {
      console.error('Failed to update settings')
    } else {
      console.log('Settings updated successfully')
    }
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
            <Switch checked={setting?.active} onChange={handleActiveChange} />
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
        <TextField fullWidth label='App ID' id='appId' />
        <TextField fullWidth label='App Token' id='appToken' />
        <TextField fullWidth label='App Secret' id='appSecret' />
        <Button variant='contained' onClick={handleSave}>
          Save
        </Button>
      </Stack>
    </>
  )
}
