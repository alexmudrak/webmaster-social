'use client'
import CheckIcon from '@mui/icons-material/Check'
import PlayArrowIcon from '@mui/icons-material/PlayArrow'
import StopIcon from '@mui/icons-material/Stop'
import IconButton from '@mui/material/IconButton'
import Link from '@mui/material/Link'
import TableCell from '@mui/material/TableCell'
import TableRow from '@mui/material/TableRow'
import * as React from 'react'

import { socialNetworksList } from '../../constants/SocialNetworks'
import formatDate from '../../utils/formatDate'
import ArticleNetworkStatusIcon from './ArticleNetworkStatusIcons'

export default function ArticleTableRow({ article }) {
  return (
    <TableRow
      key={article.id}
      sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
    >
      <TableCell component='th' scope='row'>
        {`# ${article.id}`}
      </TableCell>
      <TableCell component='th' scope='row'>
        {formatDate(article.created)}
      </TableCell>
      <TableCell align='left'>{article.project_name}</TableCell>
      <TableCell align='left'>
        <Link href='#' underline='none'>
          {article.title}
        </Link>
      </TableCell>
      <TableCell align='right'>
        {socialNetworksList.map((networkName) => {
          const networkStatus = article.network_statuses.find(
            (network) => network.name === networkName
          ) || { status: 'PENDING' }

          return (
            <ArticleNetworkStatusIcon
              key={networkName}
              status={networkStatus.status}
              name={networkName}
            />
          )
        })}
      </TableCell>
      <TableCell align='right'>
        <IconButton>
          <PlayArrowIcon />
        </IconButton>
        <IconButton>
          <StopIcon />
        </IconButton>
        <IconButton>
          <CheckIcon />
        </IconButton>
      </TableCell>
    </TableRow>
  )
}
