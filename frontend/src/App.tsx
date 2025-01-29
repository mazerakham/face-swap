import React, { useState, useEffect } from 'react'
import WelcomeScreen from './components/WelcomeScreen'
import ImageUpload from './components/ImageUpload'
import Questions from './components/Questions'
import ImageFeedback from './components/ImageFeedback'
import ImageGeneration from './components/ImageGeneration'
import FinalResult from './components/FinalResult'
import { workflowService, WorkflowStep, WorkflowState } from './service/WorkflowService'

const App: React.FC = () => {
  const [state, setState] = useState<WorkflowState>(workflowService.getState())

  useEffect(() => {
    const updateState = () => {
      setState(workflowService.getState())
    }

    // Set up an interval to check for state changes
    const interval = setInterval(updateState, 100)
    return () => clearInterval(interval)
  }, [])

  const renderCurrentStep = () => {
    switch (state.currentStep) {
      case WorkflowStep.Welcome:
        return <WelcomeScreen />
      case WorkflowStep.UploadImage:
        return <ImageUpload />
      case WorkflowStep.Questions:
        return <Questions />
      case WorkflowStep.ImageGeneration:
        return <ImageGeneration />
      case WorkflowStep.ImageFeedback:
        return <ImageFeedback />
      case WorkflowStep.FinalResult:
        return <FinalResult />
      default:
        return <WelcomeScreen />
    }
  }

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      {renderCurrentStep()}
    </div>
  )
}

export default App
