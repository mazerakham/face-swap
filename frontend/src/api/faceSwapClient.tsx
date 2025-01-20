interface SwapResponse {
  job_id: string;
}

interface SwapStatusResponse {
  status: number;
  processed?: {
    url: string;
  };
}

export class FaceSwapClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api/v1') {
    this.baseUrl = baseUrl;
    console.log('API Base URL:', process.env.REACT_APP_API_BASE_URL); // For debugging
  }
  
  async uploadFile(file: File): Promise<string> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    const data = await response.json();
    return data.url;
  }

  async initiateFaceSwap(sourceUrl: string, targetUrl: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/swap`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        source_url: sourceUrl,
        target_url: targetUrl
      }),
    });

    if (!response.ok) {
      throw new Error('Face swap failed');
    }

    const result: SwapResponse = await response.json();
    return result.job_id;
  }

  async checkSwapStatus(jobId: string): Promise<SwapStatusResponse> {
    const response = await fetch(`${this.baseUrl}/swap/${jobId}`);
    
    if (!response.ok) {
      throw new Error('Failed to check job status');
    }

    return response.json();
  }

  async waitForSwapCompletion(jobId: string, pollInterval: number = 2000): Promise<string> {
    while (true) {
      const status = await this.checkSwapStatus(jobId);
      
      if (status.status === 2 && status.processed?.url) {
        return status.processed.url;
      }
      
      if (status.status === 3 || status.status === 4) {
        throw new Error('Face swap processing failed');
      }

      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }
  }
}

export const faceSwapClient = new FaceSwapClient();
