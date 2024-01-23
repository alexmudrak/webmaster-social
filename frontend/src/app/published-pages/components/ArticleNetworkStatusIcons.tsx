import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ErrorIcon from '@mui/icons-material/Error'
import HelpOutlineIcon from '@mui/icons-material/HelpOutline'
import { Tooltip } from '@mui/material'
import * as React from 'react'

interface NetworkStatusIconProps {
  status: 'DONE' | 'ERROR' | 'PENDING'
  name: string
}
export default function ArticleNetworkStatusIcon({
  status,
  name
}: NetworkStatusIconProps) {
  let icon
  switch (status) {
    case 'DONE':
      icon = <CheckCircleIcon color='success' />
      break
    case 'ERROR':
      icon = <ErrorIcon color='error' />
      break
    default:
      icon = <HelpOutlineIcon color='disabled' />
  }

  return (
    <Tooltip title={name} placement='top'>
      {icon}
    </Tooltip>
  )
}
