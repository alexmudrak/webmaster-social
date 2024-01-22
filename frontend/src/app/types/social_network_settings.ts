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

export interface SocialAppModalProps {
  title: string
  data?: Setting[]
  open: boolean
  handleClose: () => void
  handlerSettingUpdate: (_: number, __: Setting) => void
}

export interface SocialAppProps {
  title: string
  data: Setting
  handlerSettingUpdate: (_: number, __: Setting) => void
  handlerCloseModal: () => void
}

export interface SocialAppSettingsProps {
  title: string
  data: Setting[]
}
