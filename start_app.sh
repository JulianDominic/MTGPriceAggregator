#!/bin/bash

handle_error() {
  echo "Error starting servers"
  exit 1
}

# Start the FastAPI server
cd backend || handle_error
.venv/bin/python -m uvicorn app:app &

# Start Vite
cd ../frontend || handle_error
npm run dev &

# wait for everything to start up
wait
