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

import { ArticlePageResponse } from '../types/articles'
import { Project } from '../types/project'
import { apiRenderRequest } from '../utils/apiRequest'
import ArticleTableRow from './components/ArticleTableRow'
import CollectArticlesButton from './libs/CollectArticlesButton'

async function getArticles() {
  const method = 'GET'
  const endpoint = 'articles/'
  const cache_method = process.env.NEXT_SSR_CACHE_METHOD

  const response = await apiRenderRequest(endpoint, {
    method: method,
    cache: cache_method
  })

  return response
}
async function getProjects() {
  const method = 'GET'
  const endpoint = 'projects/'
  const cache_method = process.env.NEXT_SSR_CACHE_METHOD

  const response = await apiRenderRequest(endpoint, {
    method: method,
    cache: cache_method
  })

  return response
}
export default async function PublishedPages() {
  // TODO: Add types
  const articles: ArticlePageResponse[] = await getArticles()
  const projects: Project[] = await getProjects()

  return (
    <Container maxWidth='xl' sx={{ marginTop: 2 }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <Typography variant='h4'>Collected Articles</Typography>
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
