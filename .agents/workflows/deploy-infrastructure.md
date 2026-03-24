---
description: Deploy GCP infrastructure via Terraform
---

# Deploy Infrastructure Workflow

Execute this workflow when deploying or updating GCP infrastructure.

// turbo-all

1. Verify the current git branch is NOT `main`:
   ```bash
   git branch --show-current
   ```

2. Initialize Terraform:
   ```bash
   cd infra && terraform init
   ```

3. Validate the Terraform configuration:
   ```bash
   terraform validate
   ```

4. Run a plan to preview changes (do NOT auto-apply):
   ```bash
   terraform plan -var-file=environments/staging.tfvars -out=tfplan
   ```

5. **🛑 STOP — Present the plan output to the user.** Do NOT run `terraform apply` without explicit user approval.

6. Only after user approval, apply the plan:
   ```bash
   terraform apply tfplan
   ```

7. Capture and display the Terraform outputs:
   ```bash
   terraform output
   ```

8. Update `README.md` with any new resource URLs, endpoints, or configuration requirements introduced by this deployment.
