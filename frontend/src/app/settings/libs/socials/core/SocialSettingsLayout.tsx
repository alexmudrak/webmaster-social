import {
  Button,
  Divider,
  FormControlLabel,
  Stack,
  Switch,
  Typography
} from '@mui/material'
import * as React from 'react'

import { SocialSettingsLayoutProps } from '../../../../types/social_network_settings'

export function SocialSettingsLayout({
  title,
  setting,
  handleActiveChange,
  handleSave,
  children
}: SocialSettingsLayoutProps) {
  const switchLabel = setting?.active ? 'On' : 'Off'

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
        {children}
        <Button variant='contained' onClick={handleSave}>
          Save
        </Button>
      </Stack>
    </>
  )
}
