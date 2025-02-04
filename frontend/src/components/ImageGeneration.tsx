import React, { useEffect } from 'react'
import { useWorkflow } from '../context/WorkflowContext'
import LoadingSpinner from './LoadingSpinner'

const ImageGeneration: React.FC = () => {
  const { state, generateImage } = useWorkflow()

  useEffect(() => {
    generateImage()
  }, [generateImage])

  return (
    <div>
      <h2>Generating Your Vision</h2>
      <p>Please wait while we create your personalized vision board...</p>
      
      {state.isLoading && <LoadingSpinner />}

      {state.error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          {state.error}
        </div>
      )}
    </div>
  )
}

export default ImageGeneration
