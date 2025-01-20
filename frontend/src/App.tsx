import React, { useState, useCallback } from 'react';
import './App.css';
import { faceSwapClient } from './api/faceSwapClient.tsx';

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
    return faceSwapClient.uploadFile(file);
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
      const jobId = await faceSwapClient.initiateFaceSwap(state.sourceUrl, state.targetUrl);
      const resultUrl = await faceSwapClient.waitForSwapCompletion(jobId);
      setState(prev => ({
        ...prev,
        resultUrl,
        isLoading: false
      }));
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
