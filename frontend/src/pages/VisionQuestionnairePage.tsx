import { useWorkflowStore } from '../store/workflowStore'
import { useNavigate } from 'react-router-dom'

export function VisionQuestionnairePage() {
  const { 
    visionResponses, 
    setVisionResponse, 
    nextStep, 
    previousStep 
  } = useWorkflowStore()
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    nextStep()
    navigate('/generate')
  }

  return (
    <div>
      <h1>Envision Your Future</h1>
      <p>Imagine yourself having accomplished your most ambitious life goals</p>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            What is the setting?
            <input
              type="text"
              value={visionResponses.setting}
              onChange={(e) => setVisionResponse('setting', e.target.value)}
              placeholder="e.g., A modern tech office, A mountain summit..."
              required
            />
          </label>
        </div>

        <div>
          <label>
            What are you wearing?
            <input
              type="text"
              value={visionResponses.attire}
              onChange={(e) => setVisionResponse('attire', e.target.value)}
              placeholder="e.g., A professional suit, Climbing gear..."
              required
            />
          </label>
        </div>

        <div>
          <label>
            What emotion are you expressing?
            <input
              type="text"
              value={visionResponses.emotion}
              onChange={(e) => setVisionResponse('emotion', e.target.value)}
              placeholder="e.g., Confident, Triumphant..."
              required
            />
          </label>
        </div>

        <div>
          <button type="button" onClick={() => {
            previousStep()
            navigate('/')
          }}>Back</button>
          <button type="submit">Next</button>
        </div>
      </form>
    </div>
  )
}
