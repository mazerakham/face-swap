import { create } from 'zustand'

interface VisionResponses {
  setting: string
  attire: string
  emotion: string
}

interface WorkflowState {
  baseImage: string | null
  visionResponses: VisionResponses
  generatedImage: string | null
  currentStep: number
  setBaseImage: (url: string) => void
  setVisionResponse: (key: keyof VisionResponses, value: string) => void
  setGeneratedImage: (url: string) => void
  nextStep: () => void
  previousStep: () => void
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  baseImage: null,
  visionResponses: {
    setting: '',
    attire: '',
    emotion: ''
  },
  generatedImage: null,
  currentStep: 0,

  setBaseImage: (url) => set({ baseImage: url }),
  
  setVisionResponse: (key, value) => 
    set((state) => ({
      visionResponses: {
        ...state.visionResponses,
        [key]: value
      }
    })),
  
  setGeneratedImage: (url) => set({ generatedImage: url }),
  
  nextStep: () => set((state) => ({ 
    currentStep: Math.min(state.currentStep + 1, 4)
  })),
  
  previousStep: () => set((state) => ({ 
    currentStep: Math.max(state.currentStep - 1, 0)
  }))
}))
