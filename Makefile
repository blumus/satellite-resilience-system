# Makefile for k3d + Skaffold development workflow

CLUSTER_NAME := satellite-dev
K3D_PORT := 8080:80@loadbalancer
KUBECONFIG := $(HOME)/.kube/config
# Build artifacts file for coordinating build and deploy
BUILD_ARTIFACTS := build-output.json

.PHONY: help cluster-create cluster-delete cluster-status dev build deploy clean logs

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

cluster-create: ## Create k3d cluster for development
	@echo "🔍 Checking if cluster $(CLUSTER_NAME) exists..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		echo "✅ Cluster $(CLUSTER_NAME) already exists"; \
		echo "🔧 Ensuring kubeconfig is set..."; \
		k3d kubeconfig merge $(CLUSTER_NAME) --kubeconfig-switch-context; \
	else \
		echo "🚀 Creating k3d cluster: $(CLUSTER_NAME)"; \
		k3d cluster create $(CLUSTER_NAME) \
			--port "$(K3D_PORT)" \
			--port "30080:30080@server:0" \
			--agents 1 \
			--wait; \
		echo "✅ Cluster created successfully"; \
		echo "🔧 Setting up kubeconfig..."; \
		k3d kubeconfig merge $(CLUSTER_NAME) --kubeconfig-switch-context; \
	fi
	@echo "📊 Cluster info:"
	kubectl cluster-info

cluster-delete: ## Delete k3d cluster
	@echo "🗑️  Deleting k3d cluster: $(CLUSTER_NAME)"
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		k3d cluster delete $(CLUSTER_NAME); \
		echo "✅ Cluster deleted"; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		exit 1; \
	fi

cluster-status: ## Show cluster status
	@echo "📊 k3d clusters:"
	k3d cluster list
	@echo ""
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		echo "🔧 Kubernetes context:"; \
		kubectl config current-context; \
		echo ""; \
		echo "📋 Cluster nodes:"; \
		kubectl get nodes; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		exit 1; \
	fi

dev: ## Start Skaffold development mode
	@echo "🔄 Starting Skaffold development mode..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		SKAFFOLD_PROFILE=local-k3d skaffold dev --port-forward; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi

cluster-ensure: ## Ensure cluster exists (create if needed)
	@echo "🔍 Ensuring cluster $(CLUSTER_NAME) is ready..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		echo "✅ Cluster $(CLUSTER_NAME) already exists"; \
		if ! k3d cluster list | grep "$(CLUSTER_NAME)" | grep -q "running"; then \
			echo "🔄 Starting stopped cluster..."; \
			k3d cluster start $(CLUSTER_NAME); \
		fi; \
		echo "🔧 Ensuring kubeconfig is set..."; \
		k3d kubeconfig merge $(CLUSTER_NAME) --kubeconfig-switch-context; \
	else \
		echo "🚀 Creating k3d cluster: $(CLUSTER_NAME)"; \
		k3d cluster create $(CLUSTER_NAME) \
			--port "$(K3D_PORT)" \
			--port "30080:30080@server:0" \
			--agents 1 \
			--wait; \
		echo "✅ Cluster created successfully"; \
		echo "🔧 Setting up kubeconfig..."; \
		k3d kubeconfig merge $(CLUSTER_NAME) --kubeconfig-switch-context; \
	fi

build: ## Build application with Skaffold
	@echo "🔨 Building application..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		echo "📋 Building and loading into k3d cluster..."; \
		SKAFFOLD_PROFILE=local-k3d skaffold build --file-output $(BUILD_ARTIFACTS); \
		if [ -f $(BUILD_ARTIFACTS) ]; then \
			echo "🔄 Ensuring image is loaded into k3d cluster..."; \
			IMAGE_TAG=$$(cat $(BUILD_ARTIFACTS) | python3 -c "import sys,json; data=json.load(sys.stdin); print(data['builds'][0]['tag'])"); \
			echo "📋 Loading image: $$IMAGE_TAG"; \
			k3d image import $$IMAGE_TAG -c $(CLUSTER_NAME); \
		fi; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi

deploy: ## Deploy application to cluster
	@echo "🚀 Deploying application..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		if [ -f $(BUILD_ARTIFACTS) ]; then \
			echo "📋 Deploying with previously built images..."; \
			SKAFFOLD_PROFILE=local-k3d skaffold deploy --build-artifacts $(BUILD_ARTIFACTS); \
		else \
			echo "❌ No build artifacts found. Run 'make build' first"; \
			exit 1; \
		fi; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi

run-with-ports: ## Build, deploy, and start port forwarding
	@echo "🏃 Running build and deploy with port forwarding..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		SKAFFOLD_PROFILE=local-k3d skaffold run --port-forward; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi

clean: ## Clean up deployments
	@echo "🧹 Cleaning up deployments..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		skaffold delete || true; \
		rm -f $(BUILD_ARTIFACTS); \
		echo "🧹 Cleaned up build artifacts"; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi

logs: ## Show application logs (live stream)
	@echo "📋 Application logs:"
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		kubectl logs -l app=hello-server --tail=100 -f; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi

logs-once: ## Show recent application logs (no streaming)
	@echo "📋 Recent application logs:"
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		kubectl logs -l app=hello-server --tail=50; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi

test: ## Test the hello server endpoints
	@echo "🧪 Testing hello server endpoints..."
	@echo "Testing main endpoint:"
	@curl -s http://localhost:30080/ && echo ""
	@echo "Testing health endpoint:"
	@curl -s http://localhost:30080/health && echo ""
	@echo "Testing ready endpoint:"
	@curl -s http://localhost:30080/ready && echo ""

port-forward: ## Start port forwarding (run in separate terminal)
	@echo "🔌 Starting port forwarding..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		echo "Access your app at: http://localhost:8081"; \
		kubectl port-forward service/hello-server-service 8081:8080; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi

cluster-start: ## Start stopped cluster
	@echo "🔄 Starting k3d cluster: $(CLUSTER_NAME)"
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		k3d cluster start $(CLUSTER_NAME); \
		k3d kubeconfig merge $(CLUSTER_NAME) --kubeconfig-switch-context; \
		echo "✅ Cluster started"; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		exit 1; \
	fi

cluster-stop: ## Stop running cluster
	@echo "⏸️  Stopping k3d cluster: $(CLUSTER_NAME)"
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		k3d cluster stop $(CLUSTER_NAME); \
		echo "✅ Cluster stopped"; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		exit 1; \
	fi


full-dev: cluster-ensure dev ## Ensure cluster exists and start development mode

# Development helpers
init: ## Initialize Skaffold configuration
	skaffold init --compose-file docker-compose.yml

debug: ## Start Skaffold in debug mode
	@echo "🐛 Starting debug mode..."
	@if k3d cluster list | grep -q "$(CLUSTER_NAME)"; then \
		SKAFFOLD_PROFILE=local-k3d skaffold debug --port-forward; \
	else \
		echo "❌ Cluster $(CLUSTER_NAME) does not exist"; \
		echo "💡 Run 'make cluster-create' first"; \
		exit 1; \
	fi
