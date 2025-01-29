import React, { useRef } from 'react'
import { workflowService } from '../service/WorkflowService'

const ImageUpload: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    await workflowService.uploadBaseImage(file)
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div>
      <h2>Upload Your Headshot</h2>
      <p>Please upload a clear photo of your face to begin the transformation journey.</p>
      
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        style={{ display: 'none' }}
      />
      
      <button onClick={handleClick}>
        Choose Photo
      </button>
    </div>
  )
}

export default ImageUpload
