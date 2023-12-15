import DeleteIcon from '@mui/icons-material/Delete'
import EditIcon from '@mui/icons-material/Edit'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Unstable_Grid2'
import * as React from 'react'

import ConfirmationModal from '../components/ConfirmationModal'
import ProjectAppModal from './ProjectAppModal'

interface ProjectAppSettingsProps {
  title: string
}

export default function ProjectAppSettings({ title }: ProjectAppSettingsProps) {
  const [openProjectModal, setOpenProjectModal] = React.useState(false)
  const [openDeleteConfirmationModal, setOpenDeleteConfirmationModal] =
    React.useState(false)

  const handleEditProject = () => setOpenProjectModal(true)
  const handleProjectModalClose = () => setOpenProjectModal(false)

  const handleDeleteProject = () => {
    setOpenDeleteConfirmationModal(true)
  }

  const handleDeleteConfirmation = () => {
    setOpenDeleteConfirmationModal(false)
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
              {'{added_project_date}'}
            </Typography>
            <Typography variant='h5' component='div'>
              {title}
            </Typography>
            <Typography sx={{ mb: 1.5 }} color='text.secondary'>
              {'{project_url}'}
            </Typography>
          </CardContent>
        </Box>
        <Button
          startIcon={<EditIcon />}
          sx={{ paddingX: 2 }}
          onClick={handleEditProject}
        >
          Edit
        </Button>
        <Button
          endIcon={<DeleteIcon />}
          sx={{ paddingX: 2 }}
          color='error'
          onClick={handleDeleteProject}
        >
          Delete
        </Button>
        <ProjectAppModal
          title={title}
          open={openProjectModal}
          handleClose={handleProjectModalClose}
        />
        <ConfirmationModal
          open={openDeleteConfirmationModal}
          handleConfirm={handleDeleteConfirmation}
          handleCancel={handleDeleteConfirmationCancel}
          title='Delete Project'
          message={`Are you sure you want to delete the project "${title}"?`}
        />
      </Card>
    </Grid>
  )
}
