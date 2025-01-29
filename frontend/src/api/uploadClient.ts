import { ApiClient } from './apiClient'

interface UploadResponse {
  url: string
}

export class UploadClient extends ApiClient {
  async uploadFile(file: File): Promise<string> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      body: formData
    })

    const data = await this.handleResponse<UploadResponse>(response)
    return data.url
  }
}

export const uploadClient = new UploadClient()
