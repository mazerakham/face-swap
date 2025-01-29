import { ApiClient } from './apiClient'

interface GenerateImageResponse {
  image_url: string
  revised_prompt: string
}

export class ImageGenerationClient extends ApiClient {
  async generateImage(setting: string, attire: string, emotion: string): Promise<GenerateImageResponse> {
    const response = await fetch(`${this.baseUrl}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        setting,
        attire,
        emotion
      })
    })

    return this.handleResponse<GenerateImageResponse>(response)
  }

  async refineImage(revisedPrompt: string, feedback: string): Promise<GenerateImageResponse> {
    const updatedPrompt = `${revisedPrompt} Changes requested: ${feedback}`
    const response = await fetch(`${this.baseUrl}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        prompt: updatedPrompt
      })
    })

    return this.handleResponse<GenerateImageResponse>(response)
  }
}

export const imageGenerationClient = new ImageGenerationClient()
