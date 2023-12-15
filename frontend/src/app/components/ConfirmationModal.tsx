import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Modal from '@mui/material/Modal'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import { modalStyle } from '../styles/modalStyle'

interface ConfirmationModalProps {
  open: boolean
  handleConfirm: () => void
  handleCancel: () => void
  title: string
  message: string
}

export default function ConfirmationModal({
  open,
  handleConfirm,
  handleCancel,
  title,
  message
}: ConfirmationModalProps) {
  return (
    <Modal
      open={open}
      onClose={handleCancel}
      aria-labelledby='modal-modal-title'
      aria-describedby='modal-modal-description'
    >
      <Box sx={modalStyle}>
        <Typography variant='h6' component='div' id='modal-modal-title'>
          {title}
        </Typography>
        <Typography variant='body2' id='modal-modal-description'>
          {message}
        </Typography>
        <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button onClick={handleCancel} sx={{ marginRight: 2 }}>
            Cancel
          </Button>
          <Button onClick={handleConfirm} color='error'>
            Confirm
          </Button>
        </Box>
      </Box>
    </Modal>
  )
}
