'use client'
import SettingsIcon from '@mui/icons-material/Settings'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardHeader from '@mui/material/CardHeader'
import FormControlLabel from '@mui/material/FormControlLabel'
import IconButton from '@mui/material/IconButton'
import Switch from '@mui/material/Switch'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import SocialAppModal from './SocialAppModal'

interface SocialAppSettingsProps {
  title: string
}

type SwitchStates = { [key: string]: boolean };

export default function SocialAppSettings({ title }: SocialAppSettingsProps) {
  // Just Mock Data
  const switchData: { label: string; id: string }[] = [
    { label: '{project_name_1}', id: 'project1' },
    { label: '{project_name_2}', id: 'project2' },
    { label: '{project_name_3}', id: 'project3' }
  ]

  const [openSocialAppModal, setOpenSocialAppModal] = React.useState(false)

  const handleSocialAppModalOpen = () => setOpenSocialAppModal(true)
  const handleSocialAppModalClose = () => setOpenSocialAppModal(false)

  const [switchStates, setSwitchStates] = React.useState<SwitchStates>(
    switchData.reduce((acc, switchItem) => {
      acc[switchItem.id] = false;
      return acc;
    }, {} as SwitchStates)
  );

  const handleChange =
    (id: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setSwitchStates((prevState) => ({
        ...prevState,
        [id]: event.target.checked
      }))
    }

  return (
    <Grid xs={12} sm={6} lg={3}>
      <Card>
        <CardHeader
          action={
            <IconButton aria-label='settings' onClick={handleSocialAppModalOpen}>
              <SettingsIcon />
            </IconButton>
          }
          title={title}
          subheader='{last_publish_date}'
        />
        <CardContent>
          {switchData.map((switchItem) => (
            <div key={switchItem.id}>
              <FormControlLabel
                control={
                  <Switch
                    checked={switchStates[switchItem.id]}
                    onChange={handleChange(switchItem.id)}
                    color='primary'
                    value={switchItem.id}
                  />
                }
                label={switchItem.label}
              />
            </div>
          ))}
        </CardContent>
        <SocialAppModal
          title={title}
          open={openSocialAppModal}
          handleClose={handleSocialAppModalClose}
        />
      </Card>
    </Grid>
  )
}
