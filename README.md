# face-swap

A face swapping application with a FastAPI backend and React frontend.

## Running the Backend Server

To run the backend server in development mode with auto-reload:

```bash
uvicorn face_swap.app:app --reload
```

The server will start and listen for incoming requests. Any changes to the code will automatically reload the server.

## Running the Full Stack

To run both the backend and frontend together, use:

```bash
./scripts/run_services.sh
```

This will start both the FastAPI backend server and the React frontend development server.
