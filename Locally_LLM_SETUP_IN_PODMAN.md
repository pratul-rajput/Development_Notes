# Setting Up Lightweight LLM with Podman on Windows

## Overview
This guide documents the complete process of setting up a lightweight Large Language Model (LLM) using Podman instead of Docker Desktop. This approach uses Ollama with the Phi-3 Mini model for resource-efficient local AI.

## Prerequisites
- Windows 10/11
- PowerShell
- Podman installed and configured
- WSL2 (for Podman machine)

## Step-by-Step Process

### 1. Verify Podman Installation
```powershell
# Check if Podman is installed and working
podman --version
```
**Expected output**: `podman version 5.4.0` (or similar)

### 2. Check Podman Machine Status
```powershell
# List all Podman machines and their status
podman machine list
```
**Expected output**: Should show a machine with "Currently running" status
```
NAME                    VM TYPE     CREATED       LAST UP            CPUS        MEMORY      DISK SIZE
podman-machine-default  wsl         5 months ago  Currently running  4           2GiB        100GiB
```

### 3. Pull and Run Ollama Container
```powershell
# Run Ollama service in detached mode with port mapping and volume
podman run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama docker.io/ollama/ollama
```

**What this does**:
- `-d`: Run in detached mode (background)
- `--name ollama`: Name the container "ollama"
- `-p 11434:11434`: Map port 11434 from container to host
- `-v ollama:/root/.ollama`: Create persistent volume for models
- `docker.io/ollama/ollama`: Pull from Docker Hub registry

### 4. Verify Container is Running
```powershell
# Check running containers
podman ps
```
**Expected output**: Should show ollama container with "Up" status

### 5. Download Lightweight Model
```powershell
# Download Phi-3 Mini model (3.8B parameters, ~2.2GB)
podman exec ollama ollama pull phi3:mini
```

**Alternative lightweight models**:
- `llama3.2:1b` - Even smaller (1B parameters, ~1.3GB)
- `gemma2:2b` - Google's lightweight model (2B parameters, ~1.6GB)
- `qwen2.5:1.5b` - Qwen 1.5B model (~1.5GB)

### 6. Test the Model
```powershell
# Test with a simple query
podman exec ollama ollama run phi3:mini "Hello, can you tell me what you are?"
```

## Usage Commands

### Interactive Chat
```powershell
# Start interactive chat session
podman exec -it ollama ollama run phi3:mini
```
*Type your messages and press Enter. Type `/bye` to exit.*

### Single Queries
```powershell
# Ask single questions
podman exec ollama ollama run phi3:mini "Your question here"
```

### API Access
The model is available via REST API at `http://localhost:11434`

Example using curl:
```powershell
curl -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{"model": "phi3:mini", "prompt": "Hello world", "stream": false}'
```

## Container Management

### Start/Stop/Restart
```powershell
# Stop the container
podman stop ollama

# Start the container
podman start ollama

# Restart the container
podman restart ollama

# Check container status
podman ps -a
```

### Remove Container (if needed)
```powershell
# Stop and remove container
podman stop ollama
podman rm ollama

# Remove downloaded models and volumes (optional)
podman volume rm ollama
```

## Troubleshooting

### Common Issues and Solutions

1. **"Cannot find file specified" error**
   - Ensure Podman machine is running: `podman machine start`
   - Check if WSL2 is working properly

2. **Port already in use**
   - Change port mapping: `-p 11435:11434` (use different host port)
   - Check what's using port 11434: `netstat -an | findstr 11434`

3. **Container won't start**
   - Check logs: `podman logs ollama`
   - Remove and recreate container if needed

4. **Model download fails**
   - Check internet connection
   - Try different model: `ollama pull llama3.2:1b`

### Performance Tips

1. **For even lower resource usage**:
   - Use `llama3.2:1b` instead of `phi3:mini`
   - Limit container memory: `--memory=2g`

2. **For better performance**:
   - Allocate more memory to Podman machine
   - Use SSD storage for better I/O

## Model Specifications

| Model | Size | Parameters | RAM Usage | Best For |
|-------|------|------------|-----------|----------|
| phi3:mini | ~2.2GB | 3.8B | ~4GB | General chat, coding |
| llama3.2:1b | ~1.3GB | 1B | ~2GB | Basic tasks, very low resource |
| gemma2:2b | ~1.6GB | 2B | ~3GB | Balanced performance |

## Quick Reference Commands

```powershell
# Setup (run once)
podman run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama docker.io/ollama/ollama
podman exec ollama ollama pull phi3:mini

# Daily usage
podman exec -it ollama ollama run phi3:mini              # Interactive chat
podman exec ollama ollama run phi3:mini "question"       # Single query

# Management
podman ps                    # Check status
podman stop ollama          # Stop service
podman start ollama         # Start service
```

## Notes for Future Reference

1. **Always check Podman machine status first** - If machine is stopped, start it with `podman machine start`

2. **Ollama vs Docker Desktop model-runner**: 
   - Docker Desktop's model-runner is a GUI feature
   - Ollama provides similar functionality via command line
   - Podman + Ollama is more lightweight and flexible

3. **Resource considerations**:
   - Phi-3 Mini uses ~4GB RAM when active
   - Model files persist in named volume `ollama`
   - Container auto-restarts unless explicitly stopped

4. **Security**: 
   - Service runs on localhost only by default
   - No external access unless explicitly configured
   - Models run in isolated container environment

5. **Backup/Migration**:
   - Models stored in `ollama` volume
   - Export volume: `podman volume export ollama > ollama-backup.tar`
   - Import volume: `podman volume import ollama ollama-backup.tar`

## Date Created
September 2, 2025

## Last Tested Environment
- Windows with PowerShell 5.1
- Podman version 5.4.0
- WSL2 backend
- Phi-3 Mini model
