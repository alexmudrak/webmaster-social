const apiUrl = process.env.NEXT_PUBLIC_API_URL
const apiRenderUrl = process.env.NEXT_RENDER_PUBLIC_API_URL

type RequestOptions = {
  method: string
  headers?: any
  body?: any
  cache?: any
}

const fetchWithRetry = async (
  url: string,
  options: RequestOptions,
  retries: number = 3
): Promise<any> => {
  try {
    const response = await fetch(url, options)
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    return await response.json()
  } catch (error) {
    if (retries > 0) {
      console.error('Fetch attempt failed, retrying...', error)
      return await fetchWithRetry(url, options, retries - 1)
    } else {
      console.error('All fetch attempts failed:', error)
      throw error
    }
  }
}

const apiRequest = async (
  path: string,
  options: RequestOptions,
  retries: number = 3
): Promise<any> => {
  const api_url = `${apiUrl}/${path}`
  return fetchWithRetry(api_url, options, retries)
}

const apiRenderRequest = async (
  path: string,
  options: RequestOptions,
  retries: number = 3
): Promise<any> => {
  const api_url = `${apiRenderUrl}/${path}`
  return fetchWithRetry(api_url, options, retries)
}

export { apiRenderRequest, apiRequest }
