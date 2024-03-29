import { TextField } from '@mui/material'
import * as React from 'react'

import { SocialAppProps } from '../../../types/social_network_settings'
import { SocialSettingsLayout } from './core/SocialSettingsLayout'
import { useSocialSettings } from './core/useSocialSettings'

export default function InstagramSettings(props: SocialAppProps) {
  // TODO: Change username to user_name
  // TODO: Change password to user_password
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
        label='Username'
        id='username'
        name='username'
        value={setting.settings.username}
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
        label='Session ID'
        id='sessionid'
        name='cookies.sessionid'
        value={setting.settings.cookies?.sessionid}
        onChange={handleInputChange}
      />
    </SocialSettingsLayout>
  )
}
