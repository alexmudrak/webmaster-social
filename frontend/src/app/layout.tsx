import './globals.css'

import Container from '@mui/material/Container'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import * as React from 'react'

import NavBar from './components/NavBar'

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
        <Container>{children}</Container>
      </body>
    </html>
  )
}
