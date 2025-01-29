import { ApiClient } from './apiClient'

interface SwapResponse {
  id: string
  status: string
  result_url?: string
}

export class FaceSwapClient extends ApiClient {
  async initiateFaceSwap(sourceUrl: string, targetUrl: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/swap`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        source_url: sourceUrl,
        target_url: targetUrl
      })
    })

    const result = await this.handleResponse<SwapResponse>(response)
    return result.id
  }

  async checkSwapStatus(jobId: string): Promise<SwapResponse> {
    const response = await fetch(`${this.baseUrl}/swap/${jobId}`)
    return this.handleResponse<SwapResponse>(response)
  }

  async waitForSwapCompletion(jobId: string, pollInterval: number = 2000): Promise<string> {
    while (true) {
      const status = await this.checkSwapStatus(jobId)

      if (status.status === 'completed' && status.result_url) {
        return status.result_url
      }

      if (status.status === 'failed') {
        throw new Error('Face swap processing failed')
      }

      await new Promise(resolve => setTimeout(resolve, pollInterval))
    }
  }
}

export const faceSwapClient = new FaceSwapClient()
