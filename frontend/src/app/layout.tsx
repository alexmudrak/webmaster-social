import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import NavBar from './components/NavBar'
import Box from '@mui/material/Box'
import Container from '@mui/material/Container'

const inter = Inter({ subsets: ['latin'] })

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
      <body className={inter.className}>
        <NavBar />
        <Container maxWidth='sm'>{children}</Container>
      </body>
    </html>
  )
}
