import { TextField } from '@mui/material'
import * as React from 'react'

import { SocialAppProps } from '../../../types/social_network_settings'
import { SocialSettingsLayout } from './core/SocialSettingsLayout'
import { useSocialSettings } from './core/useSocialSettings'

export default function MediumSettings(props: SocialAppProps) {
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
        label='User ID'
        id='user-id'
        name='user_id'
        value={setting.settings.user_id}
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
