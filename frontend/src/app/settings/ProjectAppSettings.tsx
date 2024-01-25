import CollectIcon from '@mui/icons-material/Archive'
import DeleteIcon from '@mui/icons-material/Delete'
import EditIcon from '@mui/icons-material/Edit'
import PublishIcon from '@mui/icons-material/Publish'
import { Box, Button, Card, CardContent, Typography } from '@mui/material'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import ConfirmationModal from '../components/ConfirmationModal'
import { Project } from '../types/project'
import ProjectAppModal from './ProjectAppModal'

export default function ProjectAppSettings({ data }: { data?: Project }) {
  const [openProjectModal, setOpenProjectModal] = React.useState(false)
  const [openDeleteConfirmationModal, setOpenDeleteConfirmationModal] =
    React.useState(false)

  const handleEditProject = () => setOpenProjectModal(true)
  const handleProjectModalClose = () => setOpenProjectModal(false)

  const handleDeleteProject = () => {
    setOpenDeleteConfirmationModal(true)
  }

  const handleCollectMaterials = async () => {
    if (data?.id) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/tasks/collect-articles/${data.id}`,
          {
            method: 'POST'
          }
        )
        if (!response.ok) {
          throw new Error('Collect article response was not ok')
        }
      } catch (error) {
        console.error('Failed to delete the project:', error)
      }
    }
  }

  const handlePublish = async () => {
    if (data?.id) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/tasks/send-article/${data.id}`,
          {
            method: 'POST'
          }
        )
        if (!response.ok) {
          throw new Error('Publish article response was not ok')
        }
      } catch (error) {
        console.error('Failed to delete the project:', error)
      }
    }
  }

  const handleDeleteConfirmation = async () => {
    setOpenDeleteConfirmationModal(false)
    if (data?.id) {
      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/projects/${data.id}`,
          {
            method: 'DELETE'
          }
        )
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
      } catch (error) {
        console.error('Failed to delete the project:', error)
      }
    }
  }

  const handleDeleteConfirmationCancel = () => {
    setOpenDeleteConfirmationModal(false)
  }

  return (
    <Grid xs={12}>
      <Card sx={{ display: 'flex' }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
          <CardContent sx={{ flex: '1 0 auto' }}>
            <Typography
              sx={{ fontSize: 14 }}
              color='text.secondary'
              gutterBottom
            >
              {`#` + data?.id}
            </Typography>
            <Typography variant='h5' component='div'>
              {data?.name}
            </Typography>
            <Typography sx={{ mb: 1.5 }} color='text.secondary'>
              {data?.url + ` (${data?.parse_type})`}
            </Typography>
          </CardContent>
        </Box>
        <Button
          startIcon={<CollectIcon />}
          sx={{ paddingX: 4 }}
          onClick={handleCollectMaterials}
        >
          Collect
        </Button>
        <Button
          startIcon={<PublishIcon />}
          sx={{ paddingX: 4 }}
          onClick={handlePublish}
        >
          Publish
        </Button>
        <Button
          startIcon={<EditIcon />}
          sx={{ paddingX: 4 }}
          onClick={handleEditProject}
        >
          Edit
        </Button>
        <Button
          endIcon={<DeleteIcon />}
          sx={{ paddingX: 4 }}
          color='error'
          onClick={handleDeleteProject}
        >
          Delete
        </Button>
        <ProjectAppModal
          data={data}
          open={openProjectModal}
          handleClose={handleProjectModalClose}
        />
        <ConfirmationModal
          open={openDeleteConfirmationModal}
          handleConfirm={handleDeleteConfirmation}
          handleCancel={handleDeleteConfirmationCancel}
          title='Delete Project'
          message={`Are you sure you want to delete the project "${data?.name}"?`}
        />
      </Card>
    </Grid>
  )
}
