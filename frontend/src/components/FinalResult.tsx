import React from 'react'
import { workflowService } from '../service/WorkflowService'

const FinalResult: React.FC = () => {
  const state = workflowService.getState()

  return (
    <div>
      <h2>Your Vision Board Complete!</h2>
      <p>Here's your personalized vision of your future self:</p>
      
      <div>
        <img 
          src={state.finalResultUrl} 
          alt="Your future self" 
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      </div>

      <div>
        <h3>Original Photos</h3>
        <div style={{ display: 'flex', gap: '20px' }}>
          <div>
            <h4>Your Photo</h4>
            <img 
              src={state.baseImageUrl} 
              alt="Your uploaded photo" 
              style={{ width: '200px', height: '200px', objectFit: 'cover' }}
            />
          </div>
          <div>
            <h4>Generated Scene</h4>
            <img 
              src={state.generatedImageUrl} 
              alt="Generated scene" 
              style={{ width: '200px', height: '200px', objectFit: 'cover' }}
            />
          </div>
        </div>
      </div>

      <div>
        <p>
          Remember: This vision board represents your potential future self. 
          Keep it as inspiration for your journey ahead!
        </p>
      </div>
    </div>
  )
}

export default FinalResult
