'use client'
import CheckIcon from '@mui/icons-material/Check'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import ErrorIcon from '@mui/icons-material/Error'
import HelpOutlineIcon from '@mui/icons-material/HelpOutline'
import LoopIcon from '@mui/icons-material/Loop'
import PlayArrowIcon from '@mui/icons-material/PlayArrow'
import StopIcon from '@mui/icons-material/Stop'
import { Divider, Tooltip } from '@mui/material'
import Container from '@mui/material/Container'
import IconButton from '@mui/material/IconButton'
import Link from '@mui/material/Link'
import Paper from '@mui/material/Paper'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Typography from '@mui/material/Typography'
import * as React from 'react'

interface StatusItem {
  name: string
  status: 'success' | 'pending' | 'error'
}

function createData(
  date: string,
  nodeTitle: string,
  networksStatuses: StatusItem[]
) {
  return { date, nodeTitle, networksStatuses }
}

const rows = [
  createData('2023-01-01', 'title of material number 1', [
    { name: 'Network 1', status: 'success' },
    { name: 'Network 2', status: 'pending' },
    { name: 'Network 3', status: 'error' }
  ]),
  createData('2023-01-02', 'Another one title 2', [
    { name: 'Network 1', status: 'success' },
    { name: 'Network 2', status: 'error' },
    { name: 'Network 3', status: 'error' }
  ]),
  createData('2023-01-03', 'One more time title 3', [
    { name: 'Network 1', status: 'success' },
    { name: 'Network 2', status: 'success' },
    { name: 'Network 3', status: 'success' }
  ]),
  createData('2023-01-04', 'And last one title 4', [
    { name: 'Network 1', status: 'success' },
    { name: 'Network 2', status: 'pending' },
    { name: 'Network 3', status: 'pending' }
  ])
]

function getNetworkStatusIcon(
  status: 'success' | 'pending' | 'error',
  name: string
): React.ReactNode {
  switch (status) {
    case 'success':
      return (
        <Tooltip title={name} placement='top'>
          <CheckCircleIcon color='success' />
        </Tooltip>
      )
    case 'pending':
      return (
        <Tooltip title={name} placement='top'>
          <HelpOutlineIcon color='disabled' />
        </Tooltip>
      )
    case 'error':
      return (
        <Tooltip title={name} placement='top'>
          <ErrorIcon color='error' />
        </Tooltip>
      )
    default:
      return null
  }
}

export default function PublishedPages() {
  const handleButtonClick = () => {
    console.log('Button clicked')
  }
  return (
    <Container maxWidth='xl' sx={{ marginTop: 2 }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <Typography variant='h4'>Published pages</Typography>
        <IconButton
          onClick={handleButtonClick}
          color='primary'
          aria-label='add project'
        >
          <LoopIcon fontSize='large' />
        </IconButton>
      </div>

      <Divider sx={{ my: 1.5 }} />

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label='simple table'>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell align='right'>Material title</TableCell>
              <TableCell align='right'>Statuses</TableCell>
              <TableCell align='right'>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow
                key={row.date}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell component='th' scope='row'>
                  {row.date}
                </TableCell>
                <TableCell align='right'>
                  <Link href='#' underline='none'>
                    {row.nodeTitle}
                  </Link>
                </TableCell>
                <TableCell align='right'>
                  {row.networksStatuses.map((item, index) => (
                    <React.Fragment key={index}>
                      {getNetworkStatusIcon(item.status, item.name)}
                      {index < row.networksStatuses.length - 1}
                    </React.Fragment>
                  ))}
                </TableCell>
                <TableCell align='right'>
                  <IconButton>
                    <PlayArrowIcon />
                  </IconButton>
                  <IconButton>
                    <StopIcon />
                  </IconButton>
                  <IconButton>
                    <CheckIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  )
}
