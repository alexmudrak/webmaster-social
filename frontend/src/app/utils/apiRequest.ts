const apiUrl = process.env.NEXT_PUBLIC_API_URL

const apiRequest = async (
  path: string,
  options: any,
  retries: number = 3
): Promise<any> => {
  const api_url = `${apiUrl}/${path}`
  try {
    const response = await fetch(api_url, options)
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    return await response.json()
  } catch (error) {
    if (retries > 0) {
      console.error('Fetch attempt failed, retrying...', error)
      return await apiRequest(path, options, retries - 1)
    } else {
      console.error('All fetch attempts failed:', error)
      throw error
    }
  }
}

export default apiRequest
