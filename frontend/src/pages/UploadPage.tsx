import { useWorkflowStore } from '../store/workflowStore'
import { useNavigate } from 'react-router-dom'
import { uploadClient } from '../api/uploadClient'

export function UploadPage() {
  const { nextStep, setBaseImage } = useWorkflowStore()
  const navigate = useNavigate()

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    try {
      const url = await uploadClient.uploadFile(file)
      setBaseImage(url)
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
