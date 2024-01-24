import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ErrorIcon from '@mui/icons-material/Error'
import CircularProgress from '@mui/material/CircularProgress';
import Divider from '@mui/material/Divider'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import Typography from '@mui/material/Typography'
import * as React from 'react'

export default function RunStatusAppDetail() {
  return (
    <List sx={{ width: '100%', bgcolor: 'background.paper' }}>
      <ListItem alignItems='flex-start'>
        <ListItemText
          primary={`{social_network_1}`}
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component='span'
                variant='body2'
                color='text.primary'
              >
                {`{status_publish_success}`}
              </Typography>
              {` - {status_date} - {text of status}`}
            </React.Fragment>
          }
        />
        <ListItemIcon>
          <CheckCircleIcon color='success' />
        </ListItemIcon>
      </ListItem>

      <Divider variant='inset' component='li' />

      <ListItem alignItems='flex-start'>
        <ListItemText
          primary={`{social_network_2}`}
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component='span'
                variant='body2'
                color='text.primary'
              >
                {`{status_publish_error}`}
              </Typography>
              {` - {status_date} - {text of status}`}
            </React.Fragment>
          }
        />
        <ListItemIcon>
          <ErrorIcon color='error' />
        </ListItemIcon>
      </ListItem>

      <Divider variant='inset' component='li' />

      <ListItem alignItems='flex-start'>
        <ListItemText
          primary={`{social_network_3}`}
          secondary={
            <React.Fragment>
              <Typography
                sx={{ display: 'inline' }}
                component='span'
                variant='body2'
                color='text.primary'
              >
                {`{status_publish_waiting}`}
              </Typography>
              {` - {status_date} - {text of status}`}
            </React.Fragment>
          }
        />
        <ListItemIcon>
          <CircularProgress color='inherit' size={20} />
        </ListItemIcon>
      </ListItem>
    </List>
  )
}
