'use client'
import PlayArrowIcon from '@mui/icons-material/PlayArrow'
import IconButton from '@mui/material/IconButton'
import Link from '@mui/material/Link'
import TableCell from '@mui/material/TableCell'
import TableRow from '@mui/material/TableRow'
import * as React from 'react'

import { socialNetworksList } from '../../constants/SocialNetworks'
import formatDate from '../../utils/formatDate'
import ArticleNetworkStatusIcon from './ArticleNetworkStatusIcons'

export default function ArticleTableRow({ article }) {
  // TODO: Add types
  const handleSendArticleToNetworks = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/articles/task/${article.id}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ articleId: article.id })
        }
      )

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      // Handle the response data as needed
      const data = await response.json()
      console.log('Play action initiated:', data)
    } catch (error) {
      console.error('Error during fetch:', error)
    }
  }
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
          ) || { status: 'PENDING', status_text: 'Pending', url: '' }

          return (
            <ArticleNetworkStatusIcon
              key={networkName}
              article_id={article.id}
              status={networkStatus}
              name={networkName}
            />
          )
        })}
      </TableCell>
      <TableCell align='right'>
        <IconButton onClick={handleSendArticleToNetworks}>
          <PlayArrowIcon />
        </IconButton>
      </TableCell>
    </TableRow>
  )
}
