import { useState } from 'react'
import { useWorkflowStore } from '../store/workflowStore'
import { useNavigate } from 'react-router-dom'
import { imageGenerationClient } from '../api/imageGenerationClient'

export function ImageRefinementPage() {
  const { 
    generatedImage,
    revisedPrompt,
    setGeneratedImage,
    nextStep,
    previousStep 
  } = useWorkflowStore()
  const navigate = useNavigate()

  const [feedback, setFeedback] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)

  const handleFeedbackSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!feedback.trim()) return

    setIsGenerating(true)
    try {
      if (!revisedPrompt) {
        throw new Error('No revised prompt available')
      }

      const { image_url, revised_prompt } = await imageGenerationClient.refineImage(
        revisedPrompt,
        feedback
      )
      setGeneratedImage(image_url, revised_prompt)
      setFeedback('')
    } catch (error) {
      console.error('Failed to refine image:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleComplete = () => {
    nextStep()
    navigate('/result')
  }

  if (!generatedImage) {
    return <div>No image to refine</div>
  }

  return (
    <div>
      <h1>Refine Your Vision</h1>
      <p>How would you like to improve this image?</p>

      <img 
        src={generatedImage} 
        alt="Current vision" 
        style={{ maxWidth: '100%' }}
      />

      <form onSubmit={handleFeedbackSubmit}>
        <textarea
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          placeholder="Describe what you'd like to change..."
          rows={4}
          style={{ width: '100%' }}
        />
        
        <div>
          <button type="button" onClick={() => {
            previousStep()
            navigate('/generate')
          }}>Back</button>
          <button 
            type="submit" 
            disabled={isGenerating || !feedback.trim()}
          >
            {isGenerating ? 'Generating...' : 'Apply Changes'}
          </button>
          <button 
            type="button" 
            onClick={handleComplete}
          >
            Continue with Current Image
          </button>
        </div>
      </form>
    </div>
  )
}
