import AutorenewIcon from '@mui/icons-material/Autorenew'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ErrorIcon from '@mui/icons-material/Error'
import HelpOutlineIcon from '@mui/icons-material/HelpOutline'
import { Tooltip } from '@mui/material'
import * as React from 'react'

import { NetworkStatusIconProps } from '../../types/articles'

export default function ArticleNetworkStatusIcon({
  article_id,
  status,
  name
}: NetworkStatusIconProps) {
  const [hovered, setHovered] = React.useState(false)

  const handleMouseEnter = () => setHovered(true)
  const handleMouseLeave = () => setHovered(false)

  const handleClick = async () => {
    // TODO: Need to refactor. Move to separate helper component
    if (status.status !== 'DONE') {
      try {
        await fetch(
          `http://localhost:8000/api/v1/articles/task/${article_id}/${name}`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: status.id })
          }
        )
        // Handle the successful response here
      } catch (error) {
        // Handle the error here
      }
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

  let tooltipContent = `#${status.id} - ${name}`
  if (status.status === 'DONE') {
    tooltipContent = (
      <React.Fragment>
        {tooltipContent} -{' '}
        <a href={status.url} target='_blank' rel='noopener noreferrer'>
          {status.url}
        </a>
      </React.Fragment>
    )
  } else {
    tooltipContent = `${tooltipContent} - ${status.status_text}`
  }

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
