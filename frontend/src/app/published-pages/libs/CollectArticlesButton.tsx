'use client'

import Button from '@mui/material/Button'

import { CollectArticlesButtonProps } from '../../types/articles'

export default function CollectArticlesButton({
  project_name,
  project_id
}: CollectArticlesButtonProps) {
  const handlePostRequest = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/tasks/collect-articles/${project_id}/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({})
        }
      )

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

    } catch (error) {
      console.error('Error during POST request:', error)
    }
  }

  return (
    <Button variant='contained' onClick={handlePostRequest}>
      Collect from {project_name}
    </Button>
  )
}
