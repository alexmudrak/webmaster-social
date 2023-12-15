'use client'
import NotificationsIcon from '@mui/icons-material/Notifications'
import AppBar from '@mui/material/AppBar'
import Badge from '@mui/material/Badge'
import Box from '@mui/material/Box'
import Fade from '@mui/material/Fade'
import IconButton from '@mui/material/IconButton'
import Paper from '@mui/material/Paper'
import Popper from '@mui/material/Popper'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import AppDrawer from './Drawer'

export default function NavBar() {
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(
    null
  )
  const [open, setOpen] = React.useState(false)

  const handleClick = () => (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget)
    setOpen((prev) => !prev)
  }
  return (
    <Box sx={{ flexGrow: 1 }}>
      <Popper
        sx={{ zIndex: 1200 }}
        open={open}
        anchorEl={anchorEl}
        placement='bottom-end'
        transition
      >
        {({ TransitionProps }) => (
          <Fade {...TransitionProps} timeout={350}>
            <Paper>
              <Typography sx={{ p: 2 }}>Notification message 1.</Typography>
              <Typography sx={{ p: 2 }}>Notification message 2.</Typography>
              <Typography sx={{ p: 2 }}>Notification message 3.</Typography>
              <Typography sx={{ p: 2 }}>Notification message 4.</Typography>
            </Paper>
          </Fade>
        )}
      </Popper>
      <AppBar
        position='static'
        sx={{ backgroundColor: 'rgb(243, 244, 246)', color: 'black' }}
        className='mb-3'
        elevation={2}
      >
        <Toolbar>
          <AppDrawer />
          <Typography
            variant='h6'
            href='/'
            component='a'
            sx={{
              flexGrow: 1,
              color: 'inherit',
              textDecoration: 'none',
              marginLeft: 2
            }}
          >
            Webmaster Social
          </Typography>

          <IconButton
            size='large'
            aria-label='show 4 new notifications'
            color='inherit'
            onClick={handleClick()}
          >
            <Badge badgeContent={4} color='error'>
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Toolbar>
      </AppBar>
    </Box>
  )
}
