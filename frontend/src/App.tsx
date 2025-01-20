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
      const response = await fetch('http://localhost:8000/api/v1/swap', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          source_url: state.sourceUrl,
          target_url: state.targetUrl
        }),
      });

      if (!response.ok) {
        throw new Error('Face swap failed');
      }

      const result = await response.json();
      const jobId = result.id;

      // Poll for results
      while (true) {
        const statusResponse = await fetch(`http://localhost:8000/api/v1/swap/${jobId}`);
        if (!statusResponse.ok) {
          throw new Error('Failed to check job status');
        }

        const statusResult = await statusResponse.json();
        
        if (statusResult.status === 2 && statusResult.processed?.url) {
          setState(prev => ({
            ...prev,
            resultUrl: statusResult.processed.url,
            isLoading: false
          }));
          break;
        } else if (statusResult.status === 3 || statusResult.status === 4) {
          throw new Error('Face swap processing failed');
        }

        // Wait 2 seconds before polling again
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
