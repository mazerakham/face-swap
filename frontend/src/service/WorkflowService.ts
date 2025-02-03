import { apiClient } from '../api/client'
import { GenerateImageRequest } from '../api/types'

export enum WorkflowStep {
  Welcome = 'welcome',
  UploadImage = 'upload',
  Questions = 'questions',
  ImageGeneration = 'generation',
  ImageFeedback = 'feedback',
  FinalResult = 'result',
}

export interface WorkflowState {
  currentStep: WorkflowStep
  baseImageUrl?: string
  userDescription?: string
  setting?: string
  outfit?: string
  emotion?: string
  generatedImageUrl?: string
  augmentedPrompt?: string
  finalResultUrl?: string
}

export interface ImageCache {
  imageUrl: string
  augmentedPrompt: string
}

export class WorkflowService {
  private state: WorkflowState = {
    currentStep: WorkflowStep.Welcome,
  }

  private imageHistory: ImageCache[] = []

  getState(): WorkflowState {
    return { ...this.state }
  }

  setState(newState: Partial<WorkflowState>): void {
    this.state = { ...this.state, ...newState }
  }

  startWorkflow(): void {
    this.setState({ currentStep: WorkflowStep.UploadImage })
  }

  async uploadBaseImage(file: File): Promise<void> {
    const uploadResponse = await apiClient.uploadImage(file)
    const describeResponse = await apiClient.describeImage(uploadResponse.url)
    
    this.setState({
      baseImageUrl: uploadResponse.url,
      userDescription: describeResponse.description,
      currentStep: WorkflowStep.Questions,
    })
  }

  setQuestionResponses(setting: string, outfit: string, emotion: string): void {
    this.setState({
      setting,
      outfit,
      emotion,
      currentStep: WorkflowStep.ImageGeneration,
    })
  }

  async generateImage(userFeedback?: string): Promise<void> {
    const request: GenerateImageRequest = {
      setting: this.state.setting!,
      outfit: this.state.outfit!,
      emotion: this.state.emotion!,
      userFeedback,
      previousAugmentedPrompt: this.state.augmentedPrompt,
      userDescription: this.state.userDescription,
    }

    const response = await apiClient.generateImage(request)
    
    this.imageHistory.push({
      imageUrl: response.imageUrl,
      augmentedPrompt: response.augmentedPrompt,
    })

    this.setState({
      generatedImageUrl: response.imageUrl,
      augmentedPrompt: response.augmentedPrompt,
      currentStep: WorkflowStep.ImageFeedback,
    })
  }

  async generateFinalResult(): Promise<void> {
    const response = await apiClient.swapFaces({
      baseImageUrl: this.state.baseImageUrl!,
      targetImageUrl: this.state.generatedImageUrl!,
    })

    this.setState({
      finalResultUrl: response.url,
      currentStep: WorkflowStep.FinalResult,
    })
  }

  getImageHistory(): ImageCache[] {
    return [...this.imageHistory]
  }
}

export const workflowService = new WorkflowService()
