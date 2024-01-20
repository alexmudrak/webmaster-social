'use client'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Divider from '@mui/material/Divider'
import FormControlLabel from '@mui/material/FormControlLabel'
import Modal from '@mui/material/Modal'
import Stack from '@mui/material/Stack'
import Switch from '@mui/material/Switch'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import { modalStyle } from '../styles/modalStyle'
import { ProjectModalProps } from '../types/project'

export default function ProjectAppModal({
  data,
  open,
  handleClose
}: ProjectModalProps) {
  const [isSwitchOn, setSwitchOn] = React.useState(true)

  const handleSwitchChange = () => {
    setSwitchOn((prev) => !prev)
  }

  const switchLabel = isSwitchOn ? 'Active' : 'Not active'
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby='modal-project-title'
      aria-describedby='modal-project-description'
    >
      <Box sx={modalStyle}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <Typography variant='h5' id='modal-project-title'>
            {data?.name || 'Add a new project'}
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
            label='Project name'
            id='projectName'
            value={data?.name}
            disabled={!isSwitchOn}
          />
          <TextField
            fullWidth
            label='Aggregation page URL'
            id='projectAggregationUrl'
            disabled={!isSwitchOn}
            value={data?.url}
          />
          <Button variant='contained' disabled={!isSwitchOn}>
            Save
          </Button>
        </Stack>
      </Box>
    </Modal>
  )
}
