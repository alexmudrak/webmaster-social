'use client'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Divider from '@mui/material/Divider'
import FormControlLabel from '@mui/material/FormControlLabel'
import Modal from '@mui/material/Modal'
import Stack from '@mui/material/Stack'
import Switch from '@mui/material/Switch'
import TextField from '@mui/material/TextField'
import ToggleButton from '@mui/material/ToggleButton'
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup'
import Typography from '@mui/material/Typography'
import * as React from 'react'

import { modalStyle } from '../styles/modalStyle'
import { Project, ProjectModalProps } from '../types/project'

const defaultProjectData: Project = {
  name: '',
  url: '',
  active: true,
  parse_type: 'html',
  parse_last_article_count: 1,
  parse_article_url_element: {
    selector: '',
    attrs: ''
  },
  parse_article_img_element: {
    selector: '',
    attrs: ''
  },
  parse_article_body_element: {
    selector: '',
    attrs: []
  }
}

export default function ProjectAppModal({
  data,
  open,
  handleClose
}: ProjectModalProps) {
  const [projectData, changeProjectData] = React.useState(
    data || defaultProjectData
  )

  const handleActiveChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      changeProjectData((prevData) => ({
        ...prevData,
        active: event.target.checked
      }))
    },
    []
  )

  const handleParseTypeChange = React.useCallback(
    (_event: React.MouseEvent<HTMLElement>, newValue: string) => {
      changeProjectData((prevData) => ({
        ...prevData,
        parse_type: newValue
      }))
    },
    []
  )

  const handleNameChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      changeProjectData((prevData) => ({
        ...prevData,
        name: event.target.value
      }))
    },
    []
  )

  const handleUrlChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      changeProjectData((prevData) => ({
        ...prevData,
        url: event.target.value
      }))
    },
    []
  )

  const handleParseArticleCountChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const value = parseInt(event.target.value, 10)
      changeProjectData((prevData) => ({
        ...prevData,
        parse_last_article_count: isNaN(value) ? 0 : value
      }))
    },
    []
  )

  const handleParseUrlSelectorChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      changeProjectData((prevData) => ({
        ...prevData,
        parse_article_url_element: {
          ...prevData.parse_article_url_element,
          selector: event.target.value
        }
      }))
    },
    []
  )

  const handleParseUrlAttrsChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      changeProjectData((prevData) => ({
        ...prevData,
        parse_article_url_element: {
          ...prevData.parse_article_url_element,
          attrs: event.target.value
        }
      }))
    },
    []
  )

  const handleParseImgSelectorChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      changeProjectData((prevData) => ({
        ...prevData,
        parse_article_img_element: {
          ...prevData.parse_article_img_element,
          selector: event.target.value
        }
      }))
    },
    []
  )

  const handleParseImgAttrsChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      changeProjectData((prevData) => ({
        ...prevData,
        parse_article_img_element: {
          ...prevData.parse_article_img_element,
          attrs: event.target.value
        }
      }))
    },
    []
  )

  const handleParseBodySelectorChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      changeProjectData((prevData) => ({
        ...prevData,
        parse_article_body_element: {
          ...prevData.parse_article_body_element,
          selector: event.target.value
        }
      }))
    },
    []
  )

  const handleParseBodyAttrsChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const attrsArray = event.target.value.split(',').filter(Boolean)
      changeProjectData((prevData) => ({
        ...prevData,
        parse_article_body_element: {
          ...prevData.parse_article_body_element,
          attrs: attrsArray.length > 0 ? attrsArray : []
        }
      }))
    },
    []
  )

  const handleSave = async () => {
    const method = projectData.id ? 'PATCH' : 'POST'
    const endpoint = projectData.id
      ? `http://localhost:8000/api/v1/projects/${projectData.id}/`
      : 'http://localhost:8000/api/v1/projects/'

    try {
      const response = await fetch(endpoint, {
        method: method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(projectData)
      })

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
    } catch (error) {
      console.error('Failed to save the project:', error)
    }
    handleClose()
  }

  const switchLabel = projectData.active ? 'Active' : 'Not active'
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby='modal-project-title'
      aria-describedby='modal-project-description'
      sx={{ overflow: 'auto' }}
    >
      <Box sx={modalStyle}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            overflow: 'auto'
          }}
        >
          <Typography variant='h5' id='modal-project-title'>
            {`#${projectData?.id} - ${projectData.name}` ||
              'Add a new project'}
          </Typography>
          <FormControlLabel
            control={
              <Switch
                checked={projectData.active}
                onChange={handleActiveChange}
              />
            }
            label={switchLabel}
          />
        </div>

        <Divider sx={{ marginY: 2 }} />

        <Stack spacing={2} direction='row' useFlexGap flexWrap='wrap'>
          <TextField
            fullWidth
            label='Project name'
            id='projectName'
            value={projectData.name}
            disabled={!projectData.active}
            onChange={handleNameChange}
          />

          <TextField
            fullWidth
            label='Aggregation page URL'
            id='projectAggregationUrl'
            disabled={!projectData.active}
            value={projectData.url}
            onChange={handleUrlChange}
          />

          <TextField
            fullWidth
            label='Parse article count'
            id='projectParseArticleCount'
            disabled={!projectData.active}
            value={projectData.parse_last_article_count || 1}
            type='number'
            InputLabelProps={{
              shrink: true
            }}
            InputProps={{
              inputProps: {
                min: 1,
                step: 1
              }
            }}
            onChange={handleParseArticleCountChange}
          />

          <ToggleButtonGroup
            color='warning'
            fullWidth
            value={projectData.parse_type}
            exclusive
            onChange={handleParseTypeChange}
            aria-label='Parse type'
          >
            <ToggleButton value='html'>HTML</ToggleButton>
            <ToggleButton value='xml' disabled>
              XML
            </ToggleButton>
          </ToggleButtonGroup>

          {projectData.parse_type === 'html' && (
            <>
              <Divider
                sx={{
                  width: '100%',
                  border: '1px solid',
                  borderColor: 'divider'
                }}
              />
              <TextField
                label='XPath URL Selector'
                id='projectParseUrlSelectorElement'
                value={projectData.parse_article_url_element.selector}
                onChange={handleParseUrlSelectorChange}
                sx={{ width: '48%' }}
              />
              <TextField
                label='XPath URL Attribute'
                id='projectParseUrlAttrElement'
                value={projectData.parse_article_url_element.attrs}
                onChange={handleParseUrlAttrsChange}
                sx={{ width: '48%' }}
              />

              <Divider
                sx={{
                  width: '100%',
                  border: '1px solid',
                  borderColor: 'divider'
                }}
              />

              <TextField
                label='XPath IMAGE Selector'
                id='projectParseImgSelectorElement'
                value={projectData.parse_article_img_element.selector}
                onChange={handleParseImgSelectorChange}
                sx={{ width: '48%' }}
              />
              <TextField
                label='XPath IMAGE Attribute'
                id='projectParseImgAttrElement'
                value={projectData.parse_article_img_element.attrs}
                onChange={handleParseImgAttrsChange}
                sx={{ width: '48%' }}
              />

              <Divider
                sx={{
                  width: '100%',
                  border: '1px solid',
                  borderColor: 'divider'
                }}
              />

              <TextField
                fullWidth
                label='XPath BODY Selector'
                id='projectParseBodySelectorElement'
                value={projectData.parse_article_body_element.selector}
                onChange={handleParseBodySelectorChange}
              />
              <TextField
                fullWidth
                multiline
                maxRows={4}
                label='XPath BODY Attributes'
                id='projectParseBodyAttrsElement'
                value={projectData.parse_article_body_element.attrs}
                onChange={handleParseBodyAttrsChange}
                helperText='Separate by comma'
              />

              <Divider
                sx={{
                  width: '100%',
                  border: '1px solid',
                  borderColor: 'divider'
                }}
              />
            </>
          )}

          <Button variant='contained' fullWidth onClick={handleSave}>
            Save
          </Button>
        </Stack>
      </Box>
    </Modal>
  )
}
