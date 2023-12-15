import Button from '@mui/material/Button'
import Divider from '@mui/material/Divider'
import FormControlLabel from '@mui/material/FormControlLabel'
import Stack from '@mui/material/Stack'
import Switch from '@mui/material/Switch'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import * as React from 'react'

interface SocialOneProps {
  title: string;
}

export default function SocialOne({ title }: SocialOneProps) {
  const [isSwitchOn, setSwitchOn] = React.useState(false)

  const handleSwitchChange = () => {
    setSwitchOn((prev) => !prev)
  }

  const switchLabel = isSwitchOn ? 'On' : 'Off'

  return (
    <>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <Typography variant='h5' id='modal-project-title'>
          {title}
        </Typography>
        <FormControlLabel
          control={
            <Switch checked={isSwitchOn} onChange={handleSwitchChange} />
          }
          label={switchLabel}
        />
      </div>

      <Divider sx={{ marginY: 2 }} />
      
      <Stack
        sx={{
          width: '100%'
        }}
        spacing={2}
      >
        <TextField
          fullWidth
          label='App ID'
          id='appId'
          disabled={!isSwitchOn}
        />
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
    </>
  )
}
