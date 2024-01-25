'use client'
import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import AppDrawer from './Drawer'

export default function NavBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
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
        </Toolbar>
      </AppBar>
    </Box>
  )
}
