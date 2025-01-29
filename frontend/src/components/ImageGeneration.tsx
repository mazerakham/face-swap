import React, { useEffect } from 'react'
import { workflowService } from '../service/WorkflowService'

const ImageGeneration: React.FC = () => {
  useEffect(() => {
    const generateInitialImage = async () => {
      try {
        await workflowService.generateImage()
      } catch (error) {
        console.error('Failed to generate initial image:', error)
      }
    }

    generateInitialImage()
  }, []) // Run once on mount

  return (
    <div>
      <h2>Generating Your Vision</h2>
      <p>Please wait while we create your personalized vision board...</p>
      <div>
        {/* Add a loading spinner or animation here if desired */}
      </div>
    </div>
  )
}

export default ImageGeneration
