# Running the DISCO-ML Prototype Tool

This document provides instructions on how to start the backend and frontend components of the DISCO-ML prototype tool.

## Prerequisites

- **GraphDB**: Ensure GraphDB is running on `http://localhost:7200`. The default repository used is `disco-ml`.
- **Node.js**: The frontend requires Node.js (managed via `nvm` in this environment).
- **Python**: The backend requires Python 3.12+ and a virtual environment.

## Starting the Backend

The backend is a FastAPI application.

1. Navigate to the `backend` directory:
   ```bash
   cd prototype-tool/backend
   ```
2. Activate the virtual environment:
   ```bash
   source .backend_venv/bin/activate
   ```
3. Start the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`.

## Starting the Frontend

The frontend is a Next.js application.

1. Navigate to the `frontend` directory:
   ```bash
   cd prototype-tool/frontend
   ```
2. (Optional) Load `nvm` if not already in your path:
   ```bash
   export NVM_DIR="$HOME/.nvm"
   [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
   nvm use default
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The application will be available at `http://localhost:3000`.

## Troubleshooting

- **GraphDB Connection**: If the backend fails to connect to GraphDB, verify that GraphDB is running and the `disco-ml` repository exists.
- **Port Conflicts**: If port 8000 or 3000 is already in use, you can specify a different port (e.g., `uvicorn main:app --port 8001` or check Next.js documentation for changing the frontend port).
