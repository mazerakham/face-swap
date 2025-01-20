import React, { useState, useCallback } from 'react';
import './App.css';

interface SwapState {
  sourceUrl?: string;
  targetUrl?: string;
  resultUrl?: string;
  isLoading: boolean;
  error?: string;
}

function App() {
  const [state, setState] = useState<SwapState>({
    isLoading: false
  });

  const uploadFile = useCallback(async (file: File): Promise<string> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:8000/api/v1/upload', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    const data = await response.json();
    return data.url;
  }, []);

  const handleFileChange = useCallback(async (event: React.ChangeEvent<HTMLInputElement>, type: 'source' | 'target') => {
    const file = event.target.files?.[0];
    if (!file) return;

    setState(prev => ({ ...prev, error: undefined, isLoading: true }));

    try {
      const url = await uploadFile(file);
      setState(prev => ({
        ...prev,
        [type === 'source' ? 'sourceUrl' : 'targetUrl']: url,
        isLoading: false
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: 'Failed to upload image',
        isLoading: false
      }));
    }
  }, [uploadFile]);

  const handleSwap = useCallback(async () => {
    if (!state.sourceUrl || !state.targetUrl) return;

    setState(prev => ({ ...prev, error: undefined, isLoading: true }));

    try {
      // Start face swap job
      const response = await fetch('http://localhost:8000/api/v1/swap', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target_url: state.targetUrl,
          face_tasks: [{
            source_url: state.sourceUrl
          }]
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to start face swap');
      }

      const { id } = await response.json();

      // Poll for results
      while (true) {
        const statusResponse = await fetch(`http://localhost:8000/api/v1/status/${id}`);
        if (!statusResponse.ok) {
          throw new Error('Failed to get status');
        }

        const result = await statusResponse.json();
        
        if (result.status === 2 && result.processed) {
          setState(prev => ({
            ...prev,
            resultUrl: result.processed.url,
            isLoading: false
          }));
          break;
        } else if (result.status === 2 || result.error) {
          throw new Error(result.error || 'Face swap failed');
        }

        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Unknown error',
        isLoading: false
      }));
    }
  }, [state.sourceUrl, state.targetUrl]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Face Swap</h1>
        
        <div className="upload-section">
          <div>
            <h3>Source Face</h3>
            <input 
              type="file" 
              accept="image/*"
              onChange={e => handleFileChange(e, 'source')}
              disabled={state.isLoading}
            />
            {state.sourceUrl && (
              <img src={state.sourceUrl} alt="Source" className="preview" />
            )}
          </div>

          <div>
            <h3>Target Image</h3>
            <input 
              type="file" 
              accept="image/*"
              onChange={e => handleFileChange(e, 'target')}
              disabled={state.isLoading}
            />
            {state.targetUrl && (
              <img src={state.targetUrl} alt="Target" className="preview" />
            )}
          </div>
        </div>

        <button 
          onClick={handleSwap}
          disabled={!state.sourceUrl || !state.targetUrl || state.isLoading}
        >
          {state.isLoading ? 'Processing...' : 'Swap Faces'}
        </button>

        {state.error && (
          <div className="error">{state.error}</div>
        )}

        {state.resultUrl && (
          <div className="result">
            <h3>Result</h3>
            <img src={state.resultUrl} alt="Result" className="preview" />
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
