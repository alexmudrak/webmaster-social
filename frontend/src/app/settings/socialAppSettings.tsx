'use client'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import FormControlLabel from '@mui/material/FormControlLabel'
import Switch from '@mui/material/Switch'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

interface SocialAppSettingsProps {
  title: string
}

export default function SocialAppSettings({ title }: SocialAppSettingsProps) {
  const [success, setSuccess] = React.useState(false)
  const [status, setStatus] = React.useState('Off')

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSuccess(event.target.checked)
    setStatus(event.target.checked ? 'Off' : 'On')
  }
  return (
    <>
      <Grid xs={12} sm={6} lg={3}>
        <Card>
          <CardContent>
            <FormControlLabel
              control={
                <Switch
                  checked={success}
                  onChange={handleChange}
                  color='primary'
                  value='dynamic-class-name'
                />
              }
              label={status}
            />
            {title}
          </CardContent>
        </Card>
      </Grid>
    </>
  )
}
