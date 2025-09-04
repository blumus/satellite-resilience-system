# Development Workflow Guide

This guide explains how to use the Makefile commands to orchestrate your k3d + Skaffold development environment for the Satellite Processing System.

## 🎯 Overview

The Makefile provides a simple interface to manage your local Kubernetes development environment using:
- **k3d** - Lightweight Kubernetes clusters in Docker
- **Skaffold** - Continuous development for Kubernetes applications
- **kubectl** - Kubernetes command-line tool
- **Docker** - Container runtime and image building

## 📋 Prerequisites

Ensure your devcontainer is built and running with all required tools:
- Docker CE
- k3d
- kubectl  
- Skaffold
- Helm
- Kustomize

## 🏗️ Architecture Overview

### Dockerfiles
- **`Dockerfile`** - Devcontainer with development tools (Docker, kubectl, Skaffold, etc.)
- **`Dockerfile.app`** - Lightweight application image for the satellite processing system

### Skaffold Configuration
- **API Version**: `skaffold/v4beta13` (compatible with Skaffold v2.16.1)
- **Build Target**: Uses `Dockerfile.app` for fast, efficient builds
- **Deploy Target**: Kubernetes manifests in `k8s/` directory
- **Port Forwarding**: Uses port 8081 for local access (avoids port 8080 conflicts)
- **Build/Deploy Separation**: `make build` + `make deploy` workflow with shared image artifacts

### Smart Cluster Management
- **Cluster Detection**: Automatically checks if cluster exists before creating
- **Cluster Recovery**: Can start stopped clusters automatically
- **Context Management**: Automatically switches to correct kubectl context

## 🚀 Quick Start

```bash
# First, create the cluster
make cluster-create

# Then start development mode
make dev
```

**What this does:**
- **`make cluster-create`**: Creates a k3d cluster named `satellite-dev`
- **`make dev`**: Builds your application, deploys to Kubernetes, starts file watching, and forwards ports

🎉 **SUCCESS! When you see:**
```
Watching for changes...
```
**Your development environment is ready!** Skaffold is now monitoring your code and will automatically rebuild and redeploy whenever you make changes.

📋 **What you'll see**: `make dev` automatically streams application logs:
```
[hello-server] Starting hello server on http://0.0.0.0:8080
[hello-server] [2025-09-04 22:49:28] "GET /health HTTP/1.1" 200 -
Watching for changes...
```

**Test your application (in a new terminal):**
```bash
# Via port-forward (automatic with make dev)
curl http://localhost:8081/         # Returns: hello
curl http://localhost:8081/health   # Returns: healthy
curl http://localhost:8081/ready    # Returns: ready

# Or direct access via NodePort
curl http://localhost:30080/        # Returns: hello
curl http://localhost:30080/health  # Returns: healthy
curl http://localhost:30080/ready   # Returns: ready
```

**Make Code Changes:**
Edit `hello_server.py` - Skaffold automatically rebuilds and redeploys in seconds!


## 📚 Available Commands

### 🔧 Cluster Management Commands

| Command | Description | Example Output |
|---------|-------------|----------------|
| `make cluster-create` | Create new k3d cluster (smart detection) | `✅ Cluster created successfully` |
| `make cluster-delete` | Delete cluster and cleanup | `✅ Cluster deleted` |
| `make cluster-start` | Start stopped cluster | `✅ Cluster satellite-dev started` |
| `make cluster-stop` | Stop running cluster | `✅ Cluster satellite-dev stopped` |
| `make cluster-status` | Show cluster status | `satellite-dev running` |

**Key Features:**
- **Smart detection** - Won't recreate existing clusters
- **Auto-configuration** - Sets up kubeconfig and context  
- **Port mapping** - Exposes 8081 (port-forward) and 30080 (NodePort)
- **Graceful failures** - Clear error messages if cluster doesn't exist

### 🔄 Development Commands

| Command | Description | What You'll See |
|---------|-------------|-----------------|
| `make dev` | Continuous development mode | `Watching for changes...` |
| `make build` | Build Docker image only | `✅ Build completed` |
| `make deploy` | Deploy using build artifacts | `✅ Deployment successful` |

**Key Behaviors:**
- **`make dev`** - Streams logs, watches files, requires existing cluster
- **Manual workflow** - `make build` → `make deploy` for step-by-step control
- **All commands** - Protected with cluster existence checks

### 🛠️ Utility Commands

| Command | Description | Quick Example |
|---------|-------------|---------------|
| `make clean` | Remove all deployments | `✅ Deployments removed` |
| `make logs` | Show live application logs | `[hello-server] GET /health 200` |
| `make port-forward` | Start port forwarding | `Access at: http://localhost:8081` |
| `make debug` | Start debug mode | `Debug port: 5678` |
| `make help` | Show all available commands | Lists all make targets |

**Key Features:**
- **All commands** - Protected with cluster existence checks
- **`make logs`** - Live streaming with health check activity
- **`make port-forward`** - Uses port 8081 to avoid conflicts



## 🔧 Configuration

### Cluster Configuration
The cluster is configured with:
- **Name**: `satellite-dev`
- **Agents**: 1 worker node
- **Ports**: 8081 (local access), 30080 (NodePort)
- **Context**: Automatically switched

### Application Configuration
- **Image**: `satellite-processor` (built from `Dockerfile.app`)
- **Base Image**: `python:3.10-slim` (lightweight)
- **Port**: 8080 (container), 8081 (local access)
- **Health Endpoints**: `/health` and `/ready`
- **Config**: Loaded from ConfigMap
- **Components**: 5 system components (file input, processing queue, picture engine, output, cleanup)

### Skaffold Configuration
- **API Version**: `skaffold/v4beta13`
- **Build Context**: Uses `Dockerfile.app` (not devcontainer)
- **Profiles**: 
  - **local-k3d**: Development profile (default)
  - **test**: Testing profile
- **Port Forwarding**: Multiple ports (8081, 8082, 8083)
- **File Watching**: Monitors `hello_server.py` and configuration files for changes

## 🐛 Troubleshooting

### Cluster Won't Start
```bash
# Check Docker is running
docker ps

# Delete and recreate cluster
make cluster-delete cluster-create
```

### Application Won't Deploy
```bash
# Check cluster status
make cluster-status

# View Skaffold logs
make dev  # Look for error messages

# Clean and redeploy
make clean
make deploy
```

### Port Already in Use
```bash
# Find process using port 8081
lsof -i :8081

# Kill the process or use different port
# Modify Makefile K3D_PORT variable
```

### Can't Access Application
```bash
# Check service status
kubectl get services

# Check pod status
kubectl get pods

# Check logs
make logs

# Test health endpoints directly
curl http://localhost:8081/health
curl http://localhost:8081/ready
```

### Build Issues
```bash
# Check if using correct Dockerfile
cat skaffold.yaml | grep dockerfile  # Should show "Dockerfile.app"

# Test build independently
make build

# Check Docker images
docker images | grep satellite-processor
```

### Port Forwarding Issues
```bash
# Check what ports are being forwarded
kubectl get services
netstat -tulpn | grep :808

# Kill processes using ports if needed
lsof -ti:8081 | xargs kill -9
```

---

## 🔧 Detailed Troubleshooting

### **❌ Issue: Terminal "Stuck" or Hanging**

**Symptoms:**
- `make dev` command doesn't return to prompt
- Terminal appears frozen after running Skaffold commands

**Cause:** 
- Skaffold runs in watch mode (continuous monitoring)
- This is NORMAL behavior, not a bug

**Solutions:**
```bash
# Option 1: Use manual workflow instead
make build deploy
make port-forward

# Option 2: Exit watch mode
Ctrl+C              # Exit current command
```

---

### **❌ Issue: Skaffold Building Wrong Dockerfile**

**Symptoms:**
- Very slow builds (minutes instead of seconds)
- Build includes Docker, kubectl, development tools
- "Building devcontainer" messages

**Diagnosis:**
```bash
# Check which Dockerfile Skaffold is using
cat skaffold.yaml | grep dockerfile
# Should show: dockerfile: Dockerfile.app
```

**Solution:**
```bash
# Verify correct configuration in skaffold.yaml
build:
  artifacts:
  - image: satellite-processor
    context: .
    docker:
      dockerfile: Dockerfile.app  # ← Should be this
```

---

### **❌ Issue: Can't Access Application**

**Symptoms:**
- `curl: Connection refused` errors
- Can't reach http://localhost:30080
- Port forwarding not working

**Diagnosis Steps:**
```bash
# 1. Check if pods are running
kubectl get pods
# Should show: hello-server-xxx Running

# 2. Check services
kubectl get services  
# Should show: hello-server-service and hello-server-nodeport

# 3. Check cluster status
make cluster-status

# 4. Test both access methods
curl http://localhost:8081/health    # Port-forward
curl http://localhost:30080/health   # NodePort
```

**Solutions:**
```bash
# If pods aren't running
make clean deploy

# If services missing
kubectl apply -f k8s/service.yaml

# If ports blocked
make port-forward  # In separate terminal
```

## 📁 File Structure

```
/home/extra/
├── Makefile              # Orchestration commands
├── skaffold.yaml         # Skaffold configuration (v4beta13)
├── Dockerfile            # Devcontainer image (development tools)
├── Dockerfile.app        # Application image (lightweight Python app)
├── k8s/                  # Kubernetes manifests
│   ├── deployment.yaml   # Application deployment
│   ├── service.yaml      # Services (ClusterIP + NodePort)
│   └── configmap.yaml    # Application configuration
├── hello_server.py       # Main application file
│   ├── main.py          # Main application with health endpoints
│   ├── input_managers/  # File input components
│   ├── processing_engines/ # Picture processing
│   ├── queue/           # Processing and cleanup queues
│   └── output/          # Output management
├── config/              # Configuration files
└── data/                # Runtime data directories
```

## 🎯 Best Practices

1. **Create cluster first** with `make cluster-create` before development work
2. **Use `make dev`** only after cluster exists (it will fail gracefully if not)
3. **Use `make logs`** to monitor application behavior
4. **Run `make cluster-status`** to verify cluster health
5. **Use `make clean`** before troubleshooting deployments
6. **Use `make cluster-delete` then `make cluster-create`** for clean slate testing
7. **Check `make help`** when unsure about commands
8. **Test health endpoints** to verify application status
9. **Use `make cluster-stop`** instead of `cluster-delete` to preserve data
10. **All cluster-dependent commands now fail gracefully** with clear error messages


## 🚀 Current System Architecture

### **Hello Server Implementation:**
The system now runs a **simple Python HTTP server** instead of the complex satellite processor:

#### **Current Working Setup:**
- **Application**: Simple hello server (`hello_server.py`)
- **Dockerfile**: `Dockerfile.app` (lightweight Python 3.10-slim)
- **Kubernetes**: Deployed as `hello-server` with health checks
- **Endpoints**:
  - `GET /` → Returns "hello"
  - `GET /health` → JSON health status
  - `GET /ready` → JSON readiness status

#### **Access Points:**
- **NodePort**: http://localhost:30080/
- **Health**: http://localhost:30080/health
- **Ready**: http://localhost:30080/ready





## 🔍 Diagnostic Commands

### **Quick System Check:**
```bash
# Full system status check
make cluster-status && echo "---" && kubectl get pods && echo "---" && make test
```

### **Detailed Diagnostics:**
```bash
# Cluster health
make cluster-status

# Application status  
kubectl get pods,services,deployments

# Recent logs
make logs-once

# Test endpoints
make test

# Check Skaffold config
skaffold diagnose
```

### **Reset Everything:**
```bash
# Nuclear option - start completely fresh
make cluster-delete
make cluster-create  
make build
make build deploy
make test
```

---

## 🎯 Prevention Strategies

### **Always Use These Commands:**
- `make cluster-ensure` - Smart cluster management
- `make test` - Verify everything works
- `make logs-once` - Check without blocking
- `make cluster-status` - Verify health

### **Avoid These Commands (Unless Needed):**
- `make dev` - Blocks terminal
- `make logs` - Blocks terminal  
- Direct `skaffold dev` - Use separate commands instead

### **Best Practices:**
1. **Test current system first** before assuming problems
2. **Use Option 1 workflow** for predictable results
3. **Check cluster status** before making changes
4. **Verify endpoints** after deployment
5. **Read logs** when things don't work as expected

---

## 🆘 Emergency Recovery

### **If Everything is Broken:**
```bash
# 1. Stop everything
make clean
make cluster-delete

# 2. Start fresh
make cluster-create

# 3. Deploy clean
make build
make build deploy

# 4. Verify working
make test
```

### **If Only Application is Broken:**
```bash
# 1. Clean deployment
make clean

# 2. Redeploy  
make build deploy

# 3. Test
make test
```

### **If Only Cluster is Broken:**
```bash
# 1. Restart cluster
make cluster-delete cluster-create

# 2. Redeploy
make build deploy

# 3. Test
make test
```

---


