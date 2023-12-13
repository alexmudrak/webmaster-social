import * as React from 'react'
import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'

export default function NavBar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar
        position='static'
        sx={{ backgroundColor: '#e0e0e0', color: 'black' }}
        className='mb-3'
      >
        <Toolbar>
          <Typography variant='h6' component='div' sx={{ flexGrow: 1 }}>
            Webmaster Social
          </Typography>
          <Button color='inherit' href='/dashboard'>
            Dashboard
          </Button>
          <Button color='inherit' href='/settings'>
            Settings
          </Button>
        </Toolbar>
      </AppBar>
    </Box>
  )
}
