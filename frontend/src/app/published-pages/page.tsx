import Container from '@mui/material/Container'
import Divider from '@mui/material/Divider'
import Paper from '@mui/material/Paper'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import ArticleTableRow from './components/ArticleTableRow'
import CollectArticlesButton from './libs/CollectArticlesButton'

export async function getArticles() {
  // TODO: Set cache from .env
  const response = await fetch('http://127.0.0.1:8000/api/v1/articles/', {
    cache: 'no-cache'
  })

  if (!response.ok) {
    throw new Error('Failed to fetch data')
  }

  return response.json()
}
export async function getProjects() {
  // TODO: Set cache from .env
  const response = await fetch('http://127.0.0.1:8000/api/v1/projects/', {
    cache: 'no-cache'
  })

  if (!response.ok) {
    throw new Error('Failed to fetch data')
  }

  return response.json()
}
export default async function PublishedPages() {
  // TODO: Add types
  const articles = await getArticles()
  const projects = await getProjects()

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
        {projects.map((project) => (
          <CollectArticlesButton
            key={project.id}
            project_name={project.name}
            project_id={project.id}
          />
        ))}
      </div>

      <Divider sx={{ my: 1.5 }} />

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label='simple table'>
          <TableHead>
            <TableRow>
              <TableCell align='center'>ID</TableCell>
              <TableCell>Date</TableCell>
              <TableCell align='left'>Project</TableCell>
              <TableCell align='left'>Article title</TableCell>
              <TableCell align='right'>Statuses</TableCell>
              <TableCell align='right'>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {articles.map((article, index) => (
              <ArticleTableRow key={index} article={article} />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  )
}
