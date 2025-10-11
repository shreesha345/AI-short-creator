#!/bin/bash

# AI Short Creator - Simple Docker Runner
# =====================================

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
MODE="production"
DETACHED=false
BUILD=false

# Show help
show_help() {
    echo -e "${GREEN}AI Short Creator - Docker Runner${NC}"
    echo "=================================="
    echo ""
    echo "Usage: ./run.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -t, --test       Run in test mode (uses mock data)"
    echo "  -d, --detached   Run in background (detached mode)"
    echo "  -b, --build      Force rebuild images"
    echo "  -s, --stop       Stop all services"
    echo "  -l, --logs       Show logs"
    echo "  -h, --help       Show this help"
    echo ""
    echo "Examples:"
    echo "  ./run.sh                    # Run in production mode"
    echo "  ./run.sh -t                 # Run in test mode"
    echo "  ./run.sh -t -d              # Run in test mode, background"
    echo "  ./run.sh -b                 # Rebuild and run"
    echo "  ./run.sh -s                 # Stop services"
    echo "  ./run.sh -l                 # Show logs"
    echo ""
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        echo "Please install Docker Desktop: https://docker.com/products/docker-desktop"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        echo -e "${RED}Error: Docker is not running${NC}"
        echo "Please start Docker Desktop and try again"
        exit 1
    fi
}

# Check if .env file exists
check_env() {
    if [[ ! -f .env ]]; then
        echo -e "${YELLOW}Warning: .env file not found${NC}"
        if [[ -f .env.example ]]; then
            echo "Creating .env from .env.example..."
            cp .env.example .env
            echo -e "${GREEN}.env file created!${NC}"
            echo -e "${YELLOW}Please edit .env and add your API keys before running again${NC}"
            exit 1
        else
            echo -e "${RED}Error: No .env.example file found${NC}"
            exit 1
        fi
    fi
}

# Stop services
stop_services() {
    echo -e "${YELLOW}Stopping AI Short Creator services...${NC}"
    docker-compose down
    echo -e "${GREEN}Services stopped!${NC}"
}

# Show logs
show_logs() {
    echo -e "${BLUE}Showing logs (Press Ctrl+C to exit)...${NC}"
    docker-compose logs -f
}

# Run the application
run_app() {
    local cmd="docker-compose"

    # Add build flag if requested
    if [[ "$BUILD" == true ]]; then
        cmd="$cmd up --build"
    else
        cmd="$cmd up"
    fi

    # Add detached flag if requested
    if [[ "$DETACHED" == true ]]; then
        cmd="$cmd -d"
    fi

    # Set environment variables
    if [[ "$MODE" == "test" ]]; then
        export TEST_MODE=true
        echo -e "${BLUE}Running in TEST MODE (uses mock data)${NC}"
    else
        echo -e "${BLUE}Running in PRODUCTION MODE${NC}"
    fi

    echo -e "${GREEN}Starting AI Short Creator...${NC}"
    echo "Command: $cmd"
    echo ""

    # Run the command
    eval $cmd

    if [[ "$DETACHED" == true ]]; then
        echo ""
        echo -e "${GREEN}Services started successfully!${NC}"
        echo "Frontend: http://localhost:3000"
        echo "Backend:  http://localhost:8000"
        echo ""
        echo "Useful commands:"
        echo "  ./run.sh -l      # Show logs"
        echo "  ./run.sh -s      # Stop services"
        echo "  docker-compose ps    # Check status"
    fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--test)
            MODE="test"
            shift
            ;;
        -d|--detached)
            DETACHED=true
            shift
            ;;
        -b|--build)
            BUILD=true
            shift
            ;;
        -s|--stop)
            check_docker
            stop_services
            exit 0
            ;;
        -l|--logs)
            check_docker
            show_logs
            exit 0
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Main execution
echo -e "${GREEN}🚀 AI Short Creator${NC}"
echo "=================="

# Run checks
check_docker

# Only check .env for production mode
if [[ "$MODE" == "production" ]]; then
    check_env
fi

# Run the application
run_app
