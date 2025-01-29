export class ApiClient {
  protected baseUrl: string

  constructor(baseUrl: string = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000') {
    this.baseUrl = baseUrl
  }

  protected async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`)
    }
    return response.json()
  }
}
