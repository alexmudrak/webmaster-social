import { TextField } from '@mui/material'
import * as React from 'react'

import { SocialAppProps } from '../../../types/social_network_settings'
import { SocialSettingsLayout } from './core/SocialSettingsLayout'
import { useSocialSettings } from './core/useSocialSettings'

export default function VkontakteSettings(props: SocialAppProps) {
  // TODO: Change app_id to client_id
  const { setting, handleActiveChange, handleInputChange, handleSave } =
    useSocialSettings(
      props.data,
      props.handlerSettingUpdate,
      props.handlerCloseModal
    )
  return (
    <SocialSettingsLayout
      {...props}
      setting={setting}
      handleActiveChange={handleActiveChange}
      handleSave={handleSave}
    >
      <TextField
        fullWidth
        label='App ID'
        id='app-id'
        name='app_id'
        value={setting.settings.app_id}
        onChange={handleInputChange}
      />
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
    </SocialSettingsLayout>
  )
}
