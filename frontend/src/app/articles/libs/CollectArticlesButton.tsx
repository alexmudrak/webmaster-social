'use client'
import Button from '@mui/material/Button'

import { CollectArticlesButtonProps } from '../../types/articles'
import { apiRequest } from '../../utils/apiRequest'

export default function CollectArticlesButton({
  project_name,
  project_id
}: CollectArticlesButtonProps) {
  const handlePostRequest = async () => {
    const method = 'POST'
    const endpoint = `tasks/collect-articles/${project_id}`

    await apiRequest(endpoint, {
      method: method
    })
  }

  return (
    <Button variant='contained' onClick={handlePostRequest}>
      Collect from {project_name}
    </Button>
  )
}
