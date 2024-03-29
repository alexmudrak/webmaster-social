import * as React from 'react'

type Cookies = {
  _auth?: string
  _pinterest_sess?: string
  _routing_id?: string
  bei?: string
  csrftoken?: string
  sessionFunnelEventLogged?: string
  ds_user_id?: string
  mid?: string
  sessionid?: string
}

type Settings = {
  client_id?: string
  client_secret?: string
  redirect_uri?: string
  refresh_token?: string
  access_token?: string
  group_id?: string | number
  author_name?: string
  user_id?: string
  app_id?: string
  board_id?: string
  cookies?: Cookies
  redirect_url?: string
  sub_reddit?: string
  password?: string
  username?: string
}

export interface Setting {
  active: boolean
  id: number | null
  name: string
  project_id?: number
  project_name: string
  settings: Settings
}

export interface GroupedSettings {
  [name: string]: Setting[]
}

export type SocialAppTitleKey =
  | 'instagram'
  | 'pinterest'
  | 'facebook'
  | 'vkontakte'
  | 'medium'
  | 'linkedin'
  | 'twitter'
  | 'telegraph'
  | 'telegram_group'
  | 'reddit'

export interface SocialAppModalProps {
  title: SocialAppTitleKey
  data?: Setting[]
  open: boolean
  handleClose: () => void
  handlerSettingUpdate: (_: number | null, __: Setting | null) => void
}

export interface SocialAppProps {
  title: string
  data: Setting
  handlerSettingUpdate: (_: number | null, __: Setting) => void
  handlerCloseModal: () => void
}

export interface SocialAppSettingsProps {
  title: SocialAppTitleKey
  data: Setting[]
}

export interface UseSocialSettingsHook {
  setting: Setting
  handleActiveChange: (_: React.ChangeEvent<HTMLInputElement>) => void
  handleInputChange: (_: React.ChangeEvent<HTMLInputElement>) => void
  handleSave: () => void
}

export interface SocialSettingsLayoutProps {
  title: string
  setting: Setting
  handleActiveChange: (_: React.ChangeEvent<HTMLInputElement>) => void
  handleSave: () => void
  children: React.ReactNode
}
