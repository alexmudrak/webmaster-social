import GitHubIcon from '@mui/icons-material/GitHub'
import Box from '@mui/material/Box'
import Container from '@mui/material/Container'
import Link from '@mui/material/Link'
import Typography from '@mui/material/Typography'
import type { Metadata } from 'next'
import * as React from 'react'

import NavBar from './components/NavBar'

export const metadata: Metadata = {
  title: 'Webmaster Social App',
  description: '...'
}

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang='en'>
      <body suppressHydrationWarning={true}>
        <NavBar />
        <Container>{children}</Container>

        <Box
          component='footer'
          sx={{
            py: 3,
            px: 2,
            mt: 'auto'
          }}
        >
          <Container maxWidth='sm'>
            <Typography variant='body1' color='text.secondary' align='center'>
              <Link
                href='https://github.com/alexmudrak/webmaster-social'
                target='_blank'
                rel='noopener noreferrer'
                color='inherit'
              >
                <GitHubIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                Webmaster Social
              </Link>
              <Typography variant='caption' display='block' gutterBottom>
                &copy; {new Date().getFullYear()}
              </Typography>
            </Typography>
          </Container>
        </Box>
      </body>
    </html>
  )
}
