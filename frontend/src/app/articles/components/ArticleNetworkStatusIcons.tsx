import AutorenewIcon from '@mui/icons-material/Autorenew'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ErrorIcon from '@mui/icons-material/Error'
import HelpOutlineIcon from '@mui/icons-material/HelpOutline'
import { Tooltip } from '@mui/material'
import * as React from 'react'

import { NetworkStatusIconProps } from '../../types/articles'
import { apiRequest } from '../../utils/apiRequest'

export default function ArticleNetworkStatusIcon({
  article_id,
  status,
  name
}: NetworkStatusIconProps) {
  const [hovered, setHovered] = React.useState(false)

  const handleMouseEnter = () => setHovered(true)
  const handleMouseLeave = () => setHovered(false)

  const handleClick = async () => {
    if (status.status !== 'DONE') {
      const method = 'POST'
      const endpoint = `articles/task/${article_id}/${name}`

      await apiRequest(endpoint, {
        method: method
      })
    }
  }

  let icon
  if (status.status === 'DONE') {
    icon = <CheckCircleIcon color='success' />
  } else if (hovered) {
    icon = <AutorenewIcon color='action' onClick={handleClick} />
  } else {
    icon =
      status.status === 'ERROR' ? (
        <ErrorIcon color='error' />
      ) : (
        <HelpOutlineIcon color='disabled' />
      )
  }

  const tooltipContent: string | React.ReactNode =
    status.status === 'DONE' ? (
      <>
        #{status.id} - {name} -{' '}
        <a href={status.url} target='_blank' rel='noopener noreferrer'>
          {status.url}
        </a>
      </>
    ) : (
      `#${status.id} - ${name} - ${status.status_text}`
    )

  return (
    <Tooltip title={tooltipContent} placement='top'>
      <div
        style={{ display: 'inline-flex', alignItems: 'center' }}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {icon}
      </div>
    </Tooltip>
  )
}
