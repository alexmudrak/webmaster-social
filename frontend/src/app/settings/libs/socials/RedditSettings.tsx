import { TextField } from '@mui/material'
import * as React from 'react'

import { SocialAppProps } from '../../../types/social_network_settings'
import { SocialSettingsLayout } from './core/SocialSettingsLayout'
import { useSocialSettings } from './core/useSocialSettings'

export default function RedditSettings(props: SocialAppProps) {
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
        label='Subreddit name'
        id='sub-reddit'
        name='sub_reddit'
        value={setting.settings.sub_reddit}
        onChange={handleInputChange}
      />
      <TextField
        fullWidth
        label='App Redirect URL'
        id='redirect-url'
        name='redirect_url'
        value={setting.settings.redirect_url}
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
    </SocialSettingsLayout>
  )
}
