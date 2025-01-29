import { useWorkflowStore } from '../store/workflowStore'
import { useNavigate } from 'react-router-dom'

export function ImageGenerationPage() {
  const { 
    visionResponses, 
    generatedImage,
    setGeneratedImage,
    nextStep,
    previousStep 
  } = useWorkflowStore()
  const navigate = useNavigate()

  const generateImage = async () => {
    try {
      // TODO: Implement actual API call
      // For now, just simulate an API call
      const mockImageUrl = 'https://placeholder.com/800x600'
      setGeneratedImage(mockImageUrl)
      nextStep()
      navigate('/refine')
    } catch (error) {
      console.error('Failed to generate image:', error)
    }
  }

  return (
    <div>
      <h1>Generating Your Vision</h1>
      
      <div>
        <h2>Your Vision Details:</h2>
        <ul>
          <li>Setting: {visionResponses.setting}</li>
          <li>Attire: {visionResponses.attire}</li>
          <li>Emotion: {visionResponses.emotion}</li>
        </ul>
      </div>

      {!generatedImage ? (
        <button onClick={generateImage}>Generate Image</button>
      ) : (
        <div>
          <img 
            src={generatedImage} 
            alt="Generated vision" 
            style={{ maxWidth: '100%' }}
          />
          <div>
            <button onClick={() => {
              previousStep()
              navigate('/vision')
            }}>Back</button>
            <button onClick={() => {
              nextStep()
              navigate('/refine')
            }}>Continue</button>
          </div>
        </div>
      )}
    </div>
  )
}
