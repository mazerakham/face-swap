import { useWorkflowStore } from '../store/workflowStore'
import { useNavigate } from 'react-router-dom'

export function UploadPage() {
  const { nextStep, setBaseImage } = useWorkflowStore()
  const navigate = useNavigate()

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        throw new Error('Upload failed')
      }

      const data = await response.json()
      setBaseImage(data.url)
      nextStep()
      navigate('/vision')
    } catch (error) {
      console.error('Failed to upload image:', error)
      // TODO: Show error to user
    }
  }

  return (
    <div>
      <h1>Upload Your Headshot</h1>
      <p>Please upload a clear photo of your face</p>
      <input 
        type="file" 
        accept="image/*"
        onChange={handleUpload}
      />
    </div>
  )
}
