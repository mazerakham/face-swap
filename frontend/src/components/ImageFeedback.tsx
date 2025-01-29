import React, { useState } from 'react'
import { workflowService } from '../service/WorkflowService'

const ImageFeedback: React.FC = () => {
  const [feedback, setFeedback] = useState('')
  const state = workflowService.getState()
  const imageHistory = workflowService.getImageHistory()

  const handleSubmitFeedback = async () => {
    if (feedback.trim()) {
      await workflowService.generateImage(feedback)
      setFeedback('')
    }
  }

  const handleFinalize = () => {
    workflowService.generateFinalResult()
  }

  return (
    <div>
      <h2>Your Vision</h2>
      
      <div>
        <img 
          src={state.generatedImageUrl} 
          alt="Generated vision" 
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      </div>

      <div>
        <h3>Previous Versions</h3>
        <div style={{ display: 'flex', gap: '10px', overflowX: 'auto' }}>
          {imageHistory.map((image, index) => (
            <img
              key={index}
              src={image.imageUrl}
              alt={`Version ${index + 1}`}
              style={{ width: '100px', height: '100px', objectFit: 'cover' }}
            />
          ))}
        </div>
      </div>

      <div>
        <h3>How would you like to adjust this image?</h3>
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="Describe any changes you'd like to make to the image..."
          rows={4}
        />
        
        <div>
          <button onClick={handleSubmitFeedback}>
            Generate New Version
          </button>
          <button onClick={handleFinalize}>
            Finalize Image
          </button>
        </div>
      </div>
    </div>
  )
}

export default ImageFeedback
