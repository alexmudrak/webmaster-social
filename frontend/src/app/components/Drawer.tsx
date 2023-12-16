'use client'
import DashboardIcon from '@mui/icons-material/Dashboard'
import LayersIcon from '@mui/icons-material/Layers'
import MenuIcon from '@mui/icons-material/Menu'
import SettingsIcon from '@mui/icons-material/Settings'
import TocIcon from '@mui/icons-material/Toc'
import Box from '@mui/material/Box'
import Divider from '@mui/material/Divider'
import Drawer from '@mui/material/Drawer'
import IconButton from '@mui/material/IconButton'
import List from '@mui/material/List'
import ListItem from '@mui/material/ListItem'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemIcon from '@mui/material/ListItemIcon'
import ListItemText from '@mui/material/ListItemText'
import * as React from 'react'

export default function AppDrawer() {
  const [state, setState] = React.useState(false)

  const toggleDrawer =
    (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
      if (
        event.type === 'keydown' &&
        ((event as React.KeyboardEvent).key === 'Tab' ||
          (event as React.KeyboardEvent).key === 'Shift')
      ) {
        return
      }

      setState(open)
    }

  const menu = () => (
    <Box
      sx={{ width: 250 }}
      role='presentation'
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        <ListItem key='dashboard' disablePadding>
          <ListItemButton component='a' href='dashboard'>
            <ListItemIcon>
              <DashboardIcon />
            </ListItemIcon>
            <ListItemText primary='Dashboard' />
          </ListItemButton>
        </ListItem>
        <ListItem key='publishedPages' disablePadding>
          <ListItemButton component='a' href='/'>
            <ListItemIcon>
              <LayersIcon />
            </ListItemIcon>
            <ListItemText primary='Published pages' />
          </ListItemButton>
        </ListItem>
      </List>

      <Divider />

      <List>
        <ListItem key='settings' disablePadding>
          <ListItemButton component='a' href='settings'>
            <ListItemIcon>
              <SettingsIcon />
            </ListItemIcon>
            <ListItemText primary='Settings' />
          </ListItemButton>
        </ListItem>

        <ListItem key='logs' disablePadding>
          <ListItemButton component='a' href='logs'>
            <ListItemIcon>
              <TocIcon />
            </ListItemIcon>
            <ListItemText primary='Logs' />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  )

  return (
    <div>
      <React.Fragment key='left'>
        <IconButton
          color='inherit'
          aria-label='open drawer'
          edge='end'
          onClick={toggleDrawer(true)}
          sx={{ ...(state && { display: 'none' }) }}
        >
          <MenuIcon />
        </IconButton>
        <Drawer anchor='left' open={state} onClose={toggleDrawer(false)}>
          {menu()}
        </Drawer>
      </React.Fragment>
    </div>
  )
}
