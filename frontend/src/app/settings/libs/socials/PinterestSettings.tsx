import { TextField } from '@mui/material'
import * as React from 'react'

import { SocialAppProps } from '../../../types/social_network_settings'
import { SocialSettingsLayout } from './core/SocialSettingsLayout'
import { useSocialSettings } from './core/useSocialSettings'

export default function PinterestSettings(props: SocialAppProps) {
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
    </SocialSettingsLayout>
  )
}
