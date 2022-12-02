## Installation

### Requirements 
- Docker
- Docker Compose plugin

### Run API

1. In /simulation directory, run 
```bash
docker compose up --build
```
2. Read docs at http://127.0.0.1:8000/api/docs 

### Project structure
- /api
    - /traffic_flow: All functions for traffic endpoint
    - router.py: API router config
- /models
    - traffic_flow.py: AgentPy model and agents for our simulation
- /core: App config and settings
