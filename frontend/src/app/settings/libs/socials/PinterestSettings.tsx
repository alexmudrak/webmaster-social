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

export default function PinterestSettings({
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
    const path = name.split('.')

    updateSetting((prevData) => {
      let updatedData = { ...prevData }

      if (path.length === 1) {
        updatedData.settings[path[0]] = value
      } else {
        let current = updatedData.settings
        for (let i = 0; i < path.length - 1; i++) {
          if (current[path[i]] === undefined) {
            current[path[i]] = {}
          }
          current = current[path[i]]
        }
        current[path[path.length - 1]] = value
      }

      return updatedData
    })
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
          label='Board ID'
          id='board-id'
          name='board_id'
          value={setting.settings.board_id}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='Auth'
          id='auth'
          name='cookies._auth'
          value={setting.settings.cookies?._auth}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          multiline
          maxRows={6}
          label='Pinterest Session'
          id='pinterest-sess'
          name='cookies._pinterest_sess'
          value={setting.settings.cookies?._pinterest_sess}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='Routing ID'
          id='routing-id'
          name='cookies._routing_id'
          value={setting.settings.cookies?._routing_id}
          onChange={handleInputChange}
        />
        <TextField
          fullWidth
          label='BEI'
          id='bei'
          name='cookies.bei'
          value={setting.settings.cookies?.bei}
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
          label='Session Funnel Event Logged'
          id='session-funnel-event-logged'
          name='cookies.sessionFunnelEventLogged'
          value={setting.settings.cookies?.sessionFunnelEventLogged}
          onChange={handleInputChange}
        />

        <Button variant='contained' onClick={handleSave}>
          Save
        </Button>
      </Stack>
    </>
  )
}
