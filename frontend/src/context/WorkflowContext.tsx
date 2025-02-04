import React, { createContext, useContext, useState, useEffect } from 'react'
import { workflowService, WorkflowState, WorkflowStep } from '../service/WorkflowService'

interface WorkflowContextType {
  state: WorkflowState
  uploadBaseImage: (file: File) => Promise<void>
  generateImage: (userFeedback?: string) => Promise<void>
  generateFinalResult: () => Promise<void>
  setQuestionResponses: (setting: string, outfit: string, emotion: string) => void
  startWorkflow: () => void
}

const WorkflowContext = createContext<WorkflowContextType | undefined>(undefined)

export const WorkflowProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<WorkflowState>({
    currentStep: WorkflowStep.Welcome,
    isLoading: false,
  })

  useEffect(() => {
    const updateState = () => {
      setState(workflowService.getState())
    }
    updateState()

    // Subscribe to state changes
    workflowService.subscribe(updateState)
    return () => workflowService.unsubscribe(updateState)
  }, [])

  const value = {
    state,
    uploadBaseImage: workflowService.uploadBaseImage.bind(workflowService),
    generateImage: workflowService.generateImage.bind(workflowService),
    generateFinalResult: workflowService.generateFinalResult.bind(workflowService),
    setQuestionResponses: workflowService.setQuestionResponses.bind(workflowService),
    startWorkflow: workflowService.startWorkflow.bind(workflowService),
  }

  return (
    <WorkflowContext.Provider value={value}>
      {children}
    </WorkflowContext.Provider>
  )
}

export const useWorkflow = () => {
  const context = useContext(WorkflowContext)
  if (!context) {
    throw new Error('useWorkflow must be used within a WorkflowProvider')
  }
  return context
}
