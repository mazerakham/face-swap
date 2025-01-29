import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useWorkflowStore } from './store/workflowStore'
import { UploadPage } from './pages/UploadPage'
import { VisionQuestionnairePage } from './pages/VisionQuestionnairePage'
import { ImageGenerationPage } from './pages/ImageGenerationPage'
import { ImageRefinementPage } from './pages/ImageRefinementPage'
import { ResultPage } from './pages/ResultPage'

function ProtectedRoute({ 
  element: Element, 
  requiredStep, 
  currentStep 
}: { 
  element: React.ComponentType
  requiredStep: number
  currentStep: number 
}) {
  if (currentStep < requiredStep) {
    return <Navigate to="/" replace />
  }
  return <Element />
}

function App() {
  const currentStep = useWorkflowStore(state => state.currentStep)

  return (
    <BrowserRouter>
      <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
        <Routes>
          <Route path="/" element={<UploadPage />} />
          <Route 
            path="/vision" 
            element={
              <ProtectedRoute 
                element={VisionQuestionnairePage} 
                requiredStep={1} 
                currentStep={currentStep} 
              />
            } 
          />
          <Route 
            path="/generate" 
            element={
              <ProtectedRoute 
                element={ImageGenerationPage} 
                requiredStep={2} 
                currentStep={currentStep} 
              />
            } 
          />
          <Route 
            path="/refine" 
            element={
              <ProtectedRoute 
                element={ImageRefinementPage} 
                requiredStep={3} 
                currentStep={currentStep} 
              />
            } 
          />
          <Route 
            path="/result" 
            element={
              <ProtectedRoute 
                element={ResultPage} 
                requiredStep={4} 
                currentStep={currentStep} 
              />
            } 
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
