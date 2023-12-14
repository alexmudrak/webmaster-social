import * as React from 'react'
import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Link from 'next/link'
import * as React from 'react'

import AppDrawer from './Drawer'

export default function NavBar() {
    const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(null)
    const [open, setOpen] = React.useState(false);

    const handleClick =
    () =>
    (event: React.MouseEvent<HTMLButtonElement>) => {
      setAnchorEl(event.currentTarget);
      setOpen((prev) => !prev);
    };
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
          <Typography variant='h6' component='div' sx={{ flexGrow: 1 }}>
            <Link href='/'>Webmaster Social</Link>
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
