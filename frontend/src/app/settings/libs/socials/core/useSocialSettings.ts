import * as React from 'react'

import {
  Setting,
  UseSocialSettingsHook
} from '../../../../types/social_network_settings'

export function useSocialSettings(
  data: Setting,
  handlerSettingUpdate: (_: number | null, __: Setting) => void,
  handlerCloseModal: () => void
): UseSocialSettingsHook {
  const [setting, updateSetting] = React.useState(data)

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
    const [field, subField] = name.split('.')

    if (subField) {
      updateSetting((prevData) => ({
        ...prevData,
        settings: {
          ...prevData.settings,
          cookies: {
            ...prevData.settings.cookies,
            [subField]: value
          }
        }
      }))
    } else {
      updateSetting((prevData) => ({
        ...prevData,
        settings: {
          ...prevData.settings,
          [field]: value
        }
      }))
    }
  }

  const handleSave = () => {
    handlerSettingUpdate(setting.id, setting)
    handlerCloseModal()
  }

  return { setting, handleActiveChange, handleInputChange, handleSave }
}
