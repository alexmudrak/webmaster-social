import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ErrorIcon from '@mui/icons-material/Error'
import CircularProgress from '@mui/material/CircularProgress'
import Divider from '@mui/material/Divider'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import { RunStatusAppDetailProps } from '../../types/dashboard'
import formatDate from '../../utils/formatDate'

export default function RunStatusAppDetail({
  networkStatuses
}: RunStatusAppDetailProps) {
  return (
    <List sx={{ width: '100%', bgcolor: 'background.paper' }}>
      {networkStatuses.map((status, index) => (
        <React.Fragment key={index}>
          <ListItem alignItems='flex-start'>
            <ListItemText
              primary={status.name}
              secondary={
                <React.Fragment>
                  <Typography
                    sx={{ display: 'inline' }}
                    component='span'
                    variant='body2'
                    color='text.primary'
                  ></Typography>
                  {` ${formatDate(status.date)} - ${status.status}`}{' '}
                  {status.status_text && ` - ${status.status_text}`}
                </React.Fragment>
              }
            />
            <ListItemIcon>
              {status.status === 'DONE' ? (
                <CheckCircleIcon color='success' />
              ) : status.status === 'ERROR' ? (
                <ErrorIcon color='error' />
              ) : (
                <CircularProgress color='inherit' size={20} />
              )}
            </ListItemIcon>
          </ListItem>
          {index < networkStatuses.length - 1 && (
            <Divider variant='inset' component='li' />
          )}
        </React.Fragment>
      ))}
    </List>
  )
}
