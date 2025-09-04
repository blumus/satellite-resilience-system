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

### Option 1: Continuous Development Mode (Recommended)
```bash
# First, create the cluster
make cluster-create

# Then start development mode
make dev
```
The workflow is:
- **`make cluster-create`**: Creates a k3d cluster named `satellite-dev`
- **`make dev`**: Builds your application, deploys to Kubernetes, starts file watching, and forwards ports

✅ **Success Indicator**: When `make dev` shows **"Watching for changes..."** - your development environment is ready! This means Skaffold is actively monitoring your code and will automatically rebuild and redeploy whenever you make changes. The terminal stays active to provide this continuous development experience. Press **Ctrl+C** when you're done coding to stop development mode.

📋 **Log Streaming**: `make dev` automatically streams application logs to your terminal. You'll see:
- **Health check activity**: Regular `/health` and `/ready` requests from Kubernetes probes
- **Your application logs**: Server startup messages and request logs  
- **Build/deploy activity**: When files change and rebuilds happen

Example log output:
```
[hello-server] Starting hello server on http://0.0.0.0:8080
[hello-server] [2025-09-04 22:49:28] "GET /health HTTP/1.1" 200 -
[hello-server] [2025-09-04 22:49:43] "GET /ready HTTP/1.1" 200 -
Watching for changes...
```

**Test your application (in a new terminal):**
```bash
# Direct access via NodePort (no port-forward needed)
curl http://localhost:30080/        # Returns: hello
curl http://localhost:30080/health  # Returns: healthy
curl http://localhost:30080/ready   # Returns: ready

# Or via port-forward (automatic with make dev)
curl http://localhost:8081/         # Returns: hello
curl http://localhost:8081/health   # Returns: healthy
curl http://localhost:8081/ready    # Returns: ready
```

### Option 2: Manual Build/Deploy Workflow
```bash
# First, create the cluster
make cluster-create

# Build, deploy, and access your application
make build deploy
make port-forward
```
This alternative workflow gives you more control:
- **`make build`**: Builds Docker image and loads it into k3d cluster
- **`make deploy`**: Deploys the built image to Kubernetes using saved build artifacts
- **`make port-forward`**: Starts port forwarding to access the application

**Note**: Use `make clean` before building if you need to remove previous deployments

**Test your application:**
```bash
# Direct access via NodePort (works immediately after make deploy)
curl http://localhost:30080/        # Returns: hello
curl http://localhost:30080/health  # Returns: healthy
curl http://localhost:30080/ready   # Returns: ready

# Or via port-forward (after running make port-forward)
curl http://localhost:8081/         # Returns: hello
curl http://localhost:8081/health   # Returns: healthy
curl http://localhost:8081/ready    # Returns: ready
```

**When to use this workflow:**
- When you want explicit control over each step
- For debugging build or deployment issues
- When you don't need continuous file watching
- For production-like deployment testing

### 3. Make Code Changes

#### For Option 1 (`make dev`) - Automatic File Watching
Edit the `hello_server.py` file - Skaffold will automatically:
- Detect file changes
- Rebuild the lightweight application image (using `Dockerfile.app`)
- Redeploy to Kubernetes
- Forward ports for immediate access

**Files watched for changes:**
- `hello_server.py` (main application file)
- `Dockerfile.app` (container configuration)
- `k8s/*.yaml` (Kubernetes manifests)

**Note**: Changes are deployed in seconds, not minutes, thanks to the optimized application Dockerfile.

#### For Option 2 (`make build deploy`) - Manual Rebuild Required
After editing `hello_server.py`, you must manually rebuild and redeploy:
```bash
# After making code changes
make build deploy
```

**No automatic file watching** - you control when rebuilds happen.

## 📚 Available Commands

### 🔧 Cluster Management Commands

| Command | Description | Use Case |
|---------|-------------|----------|
| `make cluster-create` | Create new k3d cluster (smart detection) | First time setup |
| `make cluster-delete` | Delete cluster and cleanup | Remove everything |
| `make cluster-start` | Start stopped cluster | Resume work |
| `make cluster-stop` | Stop running cluster | Pause work |
| `make cluster-status` | Show cluster status | Check what's running |

**Key Features:**
- **Smart detection** - Won't recreate existing clusters
- **Auto-configuration** - Sets up kubeconfig and context  
- **Port mapping** - Exposes 8081 (port-forward) and 30080 (NodePort)
- **Graceful failures** - Clear error messages if cluster doesn't exist

### 🔄 Development Commands

| Command | Description | File Watching | Use Case |
|---------|-------------|---------------|----------|
| `make dev` | Continuous development mode | ✅ Automatic | Daily development |
| `make build` | Build Docker image only | ❌ No | Manual build control |
| `make deploy` | Deploy using build artifacts | ❌ No | Manual deploy control |

**Key Behaviors:**
- **`make dev`** - Streams logs, watches files, requires existing cluster
- **Manual workflow** - `make build` → `make deploy` for step-by-step control
- **All commands** - Protected with cluster existence checks

### 🛠️ Utility Commands

| Command | Description | Use Case |
|---------|-------------|----------|
| `make clean` | Remove all deployments | Clean slate, troubleshooting |
| `make logs` | Show live application logs | Debugging, monitoring |
| `make port-forward` | Start port forwarding | Access application locally |
| `make debug` | Start debug mode | Advanced troubleshooting |
| `make help` | Show all available commands | Quick reference |

**Key Features:**
- **All commands** - Protected with cluster existence checks
- **`make logs`** - Live streaming with health check activity
- **`make port-forward`** - Uses port 8081 to avoid conflicts

## 🔄 Common Workflows

### Workflow Comparison

| Aspect | `make dev` (Option 1) | `make build deploy` (Option 2) |
|--------|----------------------|--------------------------------|
| **Use Case** | Continuous development | Manual control, debugging |
| **File Watching** | ✅ Automatic | ❌ Manual rebuild needed |
| **Speed** | ⚡ Instant rebuilds | 🐌 Manual rebuild cycle |
| **Control** | 🔄 Automated | 🎛️ Step-by-step control |
| **Terminal** | Stays active (watching) | Returns to prompt |
| **Log Streaming** | ✅ Automatic (live logs) | ❌ Manual (`make logs`) |
| **Best For** | Active coding sessions | Testing, debugging, CI/CD-like |

### Daily Development Workflow (Option 1: Continuous)
```bash
# Start your day - ensure cluster exists
make cluster-create  # (only needed if cluster doesn't exist)

# Start development mode  
make dev

# Make code changes to hello_server.py
# Skaffold automatically rebuilds and redeploys in seconds

# Check logs if needed (in another terminal)
make logs

# Test health endpoints
curl http://localhost:8081/health
curl http://localhost:8081/ready

# End of day - stop development (Ctrl+C) and optionally stop cluster
make cluster-stop
```

### Manual Build/Deploy Workflow (Option 2: Control)
```bash
# Start your day - ensure cluster exists
make cluster-create  # (only needed if cluster doesn't exist)

# Manual build and deploy cycle
make clean build deploy

# Start port forwarding (in background or separate terminal)
make port-forward &

# Test your application
curl http://localhost:8081/
curl http://localhost:8081/health

# Make code changes, then repeat build/deploy
make build deploy

# Check logs
make logs

# End of day - stop cluster (optional)
make cluster-stop
```

### First Time Setup
```bash
# Create cluster first
make cluster-create

# Start development
make dev

# Verify everything is working
make cluster-status
make logs

# Test the application
curl http://127.0.0.1:8082/health
```

### Testing Workflow
```bash
# Create fresh environment
make cluster-delete cluster-create

# Deploy once for testing
make build deploy

# Check application health
curl http://127.0.0.1:8082/health
curl http://127.0.0.1:8082/ready

# View logs
make logs

# Clean up
make clean
```

### Debugging Workflow
```bash
# Start debug mode
make debug

# Application runs with debug capabilities
# Set breakpoints in your IDE
# Attach debugger to port-forwarded service

# View detailed logs
make logs
```

### CI/CD Simulation
```bash
# Simulate CI/CD pipeline
make cluster-create
make build
make deploy

# Test the deployment
curl http://127.0.0.1:8082/health
curl http://127.0.0.1:8083/health  # NodePort access

# Clean up
make cluster-delete
```


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
curl http://127.0.0.1:8082/health
curl http://127.0.0.1:8082/ready
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
lsof -ti:8082 | xargs kill -9
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



# 🚨 Troubleshooting Guide

## 🔧 Common Issues & Solutions

### **❌ Issue: Terminal "Stuck" or Hanging**

**Symptoms:**
- `make dev` command doesn't return to prompt
- Terminal appears frozen after running Skaffold commands
- Can't run other commands

**Cause:** 
- Skaffold runs in watch mode (continuous monitoring)
- This is NORMAL behavior, not a bug

**Solutions:**
```bash
# Option 1: Use separate commands (RECOMMENDED)
make cluster-ensure  # Prepare cluster
make build          # Build application  
make build deploy   # Build and deploy
make test           # Test endpoints

# Option 2: Exit watch mode
Ctrl+C              # Exit current command
```

**Prevention:**
- Use Option 1 workflow commands instead of `make dev`
- Understand that `make dev` is meant to run continuously

---

### **❌ Issue: Skaffold Building Wrong Dockerfile**

**Symptoms:**
- Very slow builds (minutes instead of seconds)
- Build includes Docker, kubectl, development tools
- Large image sizes
- "Building devcontainer" messages

**Cause:**
- Skaffold using `Dockerfile` (devcontainer) instead of `Dockerfile.app`

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
```

**Solutions:**
```bash
# If pods not running:
make build deploy          # Rebuild and redeploy

# If services missing:
make clean build deploy    # Clean, build and redeploy

# If cluster issues:
make cluster-delete cluster-create               # Restart entire cluster

# Test endpoints:
make test                  # Verify all endpoints work
```

---

### **❌ Issue: Build Failures**

**Symptoms:**
- Docker build errors
- "Package not found" errors
- Image build timeouts

**Common Causes & Solutions:**

#### **Python Package Issues:**
```bash
# Check if using correct base image
grep "FROM" Dockerfile.app
# Should show: FROM python:3.10-slim

# Verify hello_server.py exists
ls -la hello_server.py
```

#### **Network/Download Issues:**
```bash
# Retry build
make build

# Check Docker daemon
docker ps

# Clear build cache if needed
docker system prune -f
```

---

### **❌ Issue: Cluster Won't Start**

**Symptoms:**
- k3d cluster creation fails
- "Cluster already exists" errors
- kubectl context issues

**Diagnosis:**
```bash
# Check existing clusters
k3d cluster list

# Check Docker is running
docker ps
```

**Solutions:**
```bash
# If cluster exists but stopped:
make cluster-start

# If cluster corrupted:
make cluster-delete
make cluster-create

# If Docker issues:
# Restart Docker daemon (depends on system)
```

---

### **❌ Issue: Port Conflicts**

**Symptoms:**
- "Port already in use" errors
- Can't bind to port 8081/30080
- Port forwarding fails

**Diagnosis:**
```bash
# Check what's using ports
lsof -i :8081
lsof -i :30080
netstat -tulpn | grep :808
```

**Solutions:**
```bash
# Kill processes using ports
lsof -ti:8081 | xargs kill -9
lsof -ti:30080 | xargs kill -9

# Or use different ports in Makefile/k8s configs
```

---

### **❌ Issue: Health Check Failures**

**Symptoms:**
- Pods stuck in "Not Ready" state
- Health check endpoints return errors
- Deployment rollout stuck

**Diagnosis:**
```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>

# Check logs
make logs-once

# Test health endpoints directly
kubectl port-forward service/hello-server-service 8081:8080 &
curl http://localhost:8081/health
```

**Solutions:**
```bash
# If hello_server.py issues:
# Check the server code is correct

# If timeout issues:
# Check resource limits in k8s/deployment.yaml

# Redeploy if needed:
make clean build deploy
```

---

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


