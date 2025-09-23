# Deployment Guide — assignment-3 Terraform

This document explains how to deploy the infrastructure in `assignment-3/terraform-scripts` (AWS, Terraform).

---

## Prerequisites

* Terraform >= 1.2 installed
* AWS CLI configured or AWS credentials in environment variables (AWS\_ACCESS\_KEY\_ID, AWS\_SECRET\_ACCESS\_KEY, AWS\_DEFAULT\_REGION)
* An AWS account with permissions to create VPCs, RDS, ECS, ALB, ECR, IAM, and related resources

---

## Safe Quickstart (Local Execution)

1. Open a terminal in `assignment-3/terraform-scripts`.

2. Initialize Terraform (this downloads providers and modules):

```bash
cd assignment-3/terraform-scripts
terraform init
```

3. Inspect `variables.tf` to see which variables are required. We do not use a `terraform.tfvars` file in this workflow — instead Terraform will prompt you for any variables that have no default when you run `plan` or `apply` (for example the RDS master password).

4. Validate and plan (Terraform will prompt for missing variables, including `db_password`):

```bash
terraform validate
terraform plan
```

5. Apply (creates resources). When prompted, provide the `db_password` interactively:

```bash
terraform apply
```

Notes: if you prefer non-interactive runs you can still pass variables on the CLI (not recommended for secrets) or export `TF_VAR_db_password` in your environment before running.

---

## Notes and Recommended Next Steps

* Use remote state for team workflows: configure an S3 backend and DynamoDB for state locking.
* Replace inline `db_password` usage with AWS Secrets Manager and reference secrets in the ECS task definition.
* Add an ALB and ECS Task/Service definitions to run your frontend and backend containers. Configure health checks and security groups accordingly.
* Add a CI/CD workflow (GitHub Actions or AWS CodePipeline + CodeBuild) to build images and update ECS services.

---

## Verification

* After apply, check outputs with `terraform output` (or view resources in the AWS console).
* Confirm RDS is available and accepts connections (use psql or a DB client). Use the private subnets — consider creating a bastion host or temporary tunnel.
* Confirm ECS cluster exists and ALB target groups register tasks when services are created.

---

## Cleanup

* To remove resources when done (Terraform will prompt for variables if required):

```bash
terraform destroy
```

---

## Troubleshooting

* If `terraform init` fails: check network access (some modules require registry.terraform.io) and provider versions.
* If RDS fails on creation: inspect `aws_db_subnet_group` and ensure subnets exist in the chosen AZs.
* If ECS tasks fail to start: check task IAM role, ENI quotas, subnet mapping, and security groups.
