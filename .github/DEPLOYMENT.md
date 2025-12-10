# GitHub Actions Deployment Setup

This repository includes automated deployment workflows to the CYBERTRON7 server.

## Workflows

### 1. Deploy to Dev (`deploy-dev.yml`)
- **Trigger**: Automatically runs on push to `dev` branch
- **Target**: Deploys to `/dev` folder on CYBERTRON7
- **Script**: Uses `_DEV.py` deployment script

### 2. Deploy to Production (`deploy-prod.yml`)
- **Trigger**: Automatically runs on push to `main` branch
- **Target**: Deploys to `/prod` folder on CYBERTRON7
- **Script**: Uses `_PROD.py` deployment script

## Required GitHub Secrets

To enable deployments, configure the following secrets in your GitHub repository:

Go to: **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Description |
|-------------|-------------|
| `CYBERTRON7_SSH_KEY` | Private SSH key for authentication to CYBERTRON7 server |
| `CYBERTRON7_HOST` | Hostname or IP address of CYBERTRON7 server |
| `CYBERTRON7_USER` | SSH username for CYBERTRON7 server |

### Setting up SSH Keys

1. On the CYBERTRON7 server, generate an SSH key pair (if not already done):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "github-actions@test77"
   ```

2. Add the public key to the server's authorized keys:
   ```bash
   cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```

3. Copy the private key and add it as `CYBERTRON7_SSH_KEY` secret in GitHub:
   ```bash
   cat ~/.ssh/id_rsa
   ```

## Deployment Scripts

### `_DEV.py`
Python script that:
- Clones or updates the repository from the `dev` branch
- Deploys code to `/dev` folder on CYBERTRON7
- Performs git operations to ensure latest code is deployed

### `_PROD.py`
Python script that:
- Clones or updates the repository from the `main` branch
- Deploys code to `/prod` folder on CYBERTRON7
- Performs git operations to ensure latest code is deployed

## Manual Deployment

Both workflows can also be triggered manually:

1. Go to **Actions** tab in GitHub
2. Select the workflow you want to run
3. Click **Run workflow** button
4. Select the branch and click **Run workflow**

## Server Requirements

The CYBERTRON7 server must have:
- Python 3.x installed
- Git installed
- Appropriate permissions to write to `/dev` and `/prod` directories
- SSH access configured

### Important Note on Deployment Directories

The deployment uses `/dev` and `/prod` directories as specified in the requirements. **Note:** `/dev` may conflict with the system device directory on Linux systems. If you encounter issues, consider modifying the deployment scripts to use alternative locations such as:
- `/opt/dev` and `/opt/prod`
- `/var/www/dev` and `/var/www/prod`
- `/home/<user>/deployments/dev` and `/home/<user>/deployments/prod`

To change the deployment directory, edit the `DEPLOY_DIR` variable in `_DEV.py` and `_PROD.py`.

## Troubleshooting

### Permission Denied Errors
Ensure the SSH user has write permissions to `/dev` and `/prod` directories:
```bash
sudo mkdir -p /dev /prod
sudo chown -R <SSH_USER>:<SSH_USER> /dev /prod
```

### Git Authentication
The deployment scripts use HTTPS cloning. If your repository is private, you may need to configure Git credentials on the server or use SSH URLs instead.

### Workflow Failures
Check the Actions tab for detailed logs. Common issues:
- Missing or incorrect secrets
- SSH connection problems
- Insufficient permissions on target directories
- Python or Git not installed on server
