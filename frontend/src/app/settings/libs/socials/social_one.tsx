import Button from '@mui/material/Button'
import FormControlLabel from '@mui/material/FormControlLabel'
import Stack from '@mui/material/Stack'
import Switch from '@mui/material/Switch'
import TextField from '@mui/material/TextField'
import * as React from 'react'

export default function SocialOne() {
  const [isSwitchOn, setSwitchOn] = React.useState(false)

  const handleSwitchChange = () => {
    setSwitchOn((prev) => !prev)
  }

  const switchLabel = isSwitchOn ? 'On' : 'Off'

  return (
    <Stack
      sx={{
        width: '100%'
      }}
      spacing={2}
    >
      <FormControlLabel
        control={<Switch checked={isSwitchOn} onChange={handleSwitchChange} />}
        label={switchLabel}
      />
      <TextField fullWidth label='App ID' id='appId' disabled={!isSwitchOn} />
      <TextField
        fullWidth
        label='App Token'
        id='appToken'
        disabled={!isSwitchOn}
      />
      <TextField
        fullWidth
        label='App Secret'
        id='appSecret'
        disabled={!isSwitchOn}
      />
      <Button variant='contained' disabled={!isSwitchOn}>
        Save
      </Button>
    </Stack>
  )
}
