export interface ImageGenerationResponse {
  imageUrl: string
  augmentedPrompt: string
}

export interface FaceSwapResponse {
  url: string
  status: string
}

export interface UploadResponse {
  url: string
}

export interface GenerateImageRequest {
  setting: string
  outfit: string
  emotion: string
  userFeedback?: string
  previousAugmentedPrompt?: string
}

export interface FaceSwapRequest {
  source_url: string
  target_url: string
}
