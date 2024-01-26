import { Box, Divider, Modal, Tab, Tabs } from '@mui/material'
import * as React from 'react'

import a11yProps from '../../../components/a11Props'
import TabPanel from '../../../components/TabPanel'
import { modalStyle } from '../../../styles/modalStyle'
import { SocialAppModalProps } from '../../../types/social_network_settings'
import FacebookSettings from '../../libs/socials/FacebookSettings'
import InstagramSettings from '../../libs/socials/InstagramSettings'
import LinkedInSettings from '../../libs/socials/LinkedInSettings'
import MediumSettings from '../../libs/socials/MediumSettings'
import PinterestSettings from '../../libs/socials/PinterestSettings'
import RedditSettings from '../../libs/socials/RedditSettings'
import TelegramGroupSettings from '../../libs/socials/TelegramGroupSettings'
import TelegraphSettings from '../../libs/socials/TelegraphSettings'
import TwitterSettings from '../../libs/socials/TwitterSettings'
import VkontakteSettings from '../../libs/socials/VkontakteSettings'

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

  const SocialComponent = React.useMemo(() => {
    const components = {
      instagram: InstagramSettings,
      pinterest: PinterestSettings,
      facebook: FacebookSettings,
      vkontakte: VkontakteSettings,
      medium: MediumSettings,
      linkedin: LinkedInSettings,
      twitter: TwitterSettings,
      telegraph: TelegraphSettings,
      telegram_group: TelegramGroupSettings,
      reddit: RedditSettings
    }

    return components[title] || null
  }, [title])

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
              key={setting.id || `setting-${index}`}
              label={setting.project_name}
              {...a11yProps(index)}
            />
          ))}
        </Tabs>

        <Divider sx={{ my: 1.5 }} />

        {data.map((setting, index) => (
          <TabPanel
            key={setting.id || `setting-${index}`}
            value={valueTab}
            index={index}
          >
            {SocialComponent ? (
              <SocialComponent
                title={title}
                data={setting}
                handlerSettingUpdate={handlerSettingUpdate}
                handlerCloseModal={handleClose}
              />
            ) : null}
          </TabPanel>
        ))}
      </Box>
    </Modal>
  )
}
