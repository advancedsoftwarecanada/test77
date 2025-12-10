#!/usr/bin/env python3
"""
Development deployment script for CYBERTRON7 server.
This script pulls the latest code from the 'dev' branch and deploys it to /dev folder.
"""

import os
import subprocess
import sys
from pathlib import Path

# Configuration
REPO_URL = "https://github.com/advancedsoftwarecanada/test77.git"
BRANCH = "dev"
DEPLOY_DIR = "/dev"

def run_command(command, cwd=None):
    """Execute a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        return e.returncode

def main():
    """Main deployment function for dev environment."""
    print(f"Starting deployment to {DEPLOY_DIR} from {BRANCH} branch...")
    
    # Create deploy directory if it doesn't exist
    deploy_path = Path(DEPLOY_DIR)
    
    if not deploy_path.exists():
        print(f"Creating directory: {DEPLOY_DIR}")
        deploy_path.mkdir(parents=True, exist_ok=True)
    
    # Check if it's already a git repository
    git_dir = deploy_path / ".git"
    
    if git_dir.exists():
        print(f"Repository exists in {DEPLOY_DIR}, updating...")
        # Fetch latest changes
        run_command("git fetch origin", cwd=DEPLOY_DIR)
        # Reset to latest branch state
        run_command(f"git reset --hard origin/{BRANCH}", cwd=DEPLOY_DIR)
        # Clean untracked files
        run_command("git clean -fd", cwd=DEPLOY_DIR)
    else:
        print(f"Cloning repository to {DEPLOY_DIR}...")
        # Clone the repository
        run_command(f"git clone --branch {BRANCH} {REPO_URL} {DEPLOY_DIR}")
    

    
    # Display current commit
    print("\nCurrent deployment commit:")
    run_command("git log -1 --oneline", cwd=DEPLOY_DIR)
    
    print(f"\nDeployment to {DEPLOY_DIR} completed successfully!")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"Deployment failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
