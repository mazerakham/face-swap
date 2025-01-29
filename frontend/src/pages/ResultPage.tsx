import { useEffect, useState } from 'react'
import { useWorkflowStore } from '../store/workflowStore'
import { useNavigate } from 'react-router-dom'

export function ResultPage() {
  const { baseImage, generatedImage, previousStep } = useWorkflowStore()
  const navigate = useNavigate()
  const [finalImage, setFinalImage] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(true)

  useEffect(() => {
    const performFaceSwap = async () => {
      if (!baseImage || !generatedImage) return

      try {
        // TODO: Implement actual face swap API call
        // For now, just simulate an API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        setFinalImage('https://placeholder.com/800x600')
      } catch (error) {
        console.error('Failed to perform face swap:', error)
      } finally {
        setIsProcessing(false)
      }
    }

    performFaceSwap()
  }, [baseImage, generatedImage])

  if (!baseImage || !generatedImage) {
    return <div>Missing required images</div>
  }

  return (
    <div>
      <h1>Your Vision, Realized</h1>
      
      {isProcessing ? (
        <div>Creating your personalized vision...</div>
      ) : finalImage ? (
        <div>
          <img 
            src={finalImage} 
            alt="Your personalized vision" 
            style={{ maxWidth: '100%' }}
          />
          <div>
            <button onClick={() => {
              previousStep()
              navigate('/refine')
            }}>Back</button>
            <button onClick={() => window.location.reload()}>
              Start Over
            </button>
            {/* TODO: Add download/share functionality */}
          </div>
        </div>
      ) : (
        <div>Failed to create final image</div>
      )}
    </div>
  )
}
