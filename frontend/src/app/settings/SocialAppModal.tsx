import { Box, Divider, Modal, Tab, Tabs } from '@mui/material'
import * as React from 'react'

import a11yProps from '../components/a11Props'
import TabPanel from '../components/TabPanel'
import { modalStyle } from '../styles/modalStyle'
import {
  SocialAppModalProps,
  SocialAppProps
} from '../types/social_network_settings'
import FacebookSettings from './libs/socials/FacebookSettings'
import InstagramSettings from './libs/socials/InstagramSettings'
import LinkedInSettings from './libs/socials/LinkedInSettings'
import MediumSettings from './libs/socials/MediumSettings'
import PinterestSettings from './libs/socials/PinterestSettings'
import TwitterSettings from './libs/socials/TwitterSettings'
import VkontakteSettings from './libs/socials/VkontakteSettings'

// TODO: Need to refactor
const FacebookSettingsMemo = React.memo(FacebookSettings)
const LinkedInSettingsMemo = React.memo(LinkedInSettings)
const InstagramSettingsMemo = React.memo(InstagramSettings)
const MediumSettingsMemo = React.memo(MediumSettings)
const PinterestSettingsMemo = React.memo(PinterestSettings)
const TwitterSettingsMemo = React.memo(TwitterSettings)
const VkontakteSettingsMemo = React.memo(VkontakteSettings)

const renderSocialComponent = ({
  title,
  data,
  handlerSettingUpdate,
  handlerCloseModal
}: SocialAppProps) => {
  switch (title) {
    case 'instagram':
      return (
        <InstagramSettingsMemo
          title={title}
          data={data}
          handlerSettingUpdate={handlerSettingUpdate}
          handlerCloseModal={handlerCloseModal}
        />
      )
    case 'pinterest':
      return (
        <PinterestSettingsMemo
          title={title}
          data={data}
          handlerSettingUpdate={handlerSettingUpdate}
          handlerCloseModal={handlerCloseModal}
        />
      )
    case 'facebook':
      return (
        <FacebookSettingsMemo
          title={title}
          data={data}
          handlerSettingUpdate={handlerSettingUpdate}
          handlerCloseModal={handlerCloseModal}
        />
      )
    case 'vkontakte':
      return (
        <VkontakteSettingsMemo
          title={title}
          data={data}
          handlerSettingUpdate={handlerSettingUpdate}
          handlerCloseModal={handlerCloseModal}
        />
      )
    case 'medium':
      return (
        <MediumSettingsMemo
          title={title}
          data={data}
          handlerSettingUpdate={handlerSettingUpdate}
          handlerCloseModal={handlerCloseModal}
        />
      )
    case 'linkedin':
      return (
        <LinkedInSettingsMemo
          title={title}
          data={data}
          handlerSettingUpdate={handlerSettingUpdate}
          handlerCloseModal={handlerCloseModal}
        />
      )
    case 'twitter':
      return (
        <TwitterSettingsMemo
          title={title}
          data={data}
          handlerSettingUpdate={handlerSettingUpdate}
          handlerCloseModal={handlerCloseModal}
        />
      )
    default:
      return null
  }
}

export default function SocialAppModal({
  title,
  data,
  open,
  handleClose,
  handlerSettingUpdate
}: SocialAppModalProps) {
  const [valueTab, setValueTab] = React.useState(0)

  const handleChangeTab = (_: React.SyntheticEvent, newValue: number) => {
    setValueTab(newValue)
  }

  if (!data) {
    return null
  }

  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby='modal-social-title'
      aria-describedby='modal-social-description'
      style={{ overflow: 'scroll' }}
    >
      <Box sx={modalStyle}>
        <Tabs
          value={valueTab}
          onChange={handleChangeTab}
          aria-label='basic tabs example'
        >
          {data.map((setting, index) => (
            <Tab
              key={setting.id !== null ? setting.id : `setting-${index}`}
              label={setting.project_name}
              {...a11yProps(index)}
            />
          ))}
        </Tabs>

        <Divider sx={{ my: 1.5 }} />

        {data.map((setting, index) => (
          <TabPanel
            key={setting.id !== null ? setting.id : `setting-${index}`}
            value={valueTab}
            index={index}
          >
            {renderSocialComponent({
              title: title,
              data: setting,
              handlerSettingUpdate: handlerSettingUpdate,
              handlerCloseModal: handleClose
            })}
          </TabPanel>
        ))}
      </Box>
    </Modal>
  )
}
