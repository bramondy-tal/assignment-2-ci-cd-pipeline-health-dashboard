# Infra Terraform for assignment-2

This folder contains Terraform configuration to provision AWS infrastructure for the CI/CD pipeline health dashboard project.

What's included:
- VPC (public + private subnets, NAT)
- RDS PostgreSQL instance
- ECS cluster (Fargate-ready)

Quickstart:
1. Install Terraform >= 1.2
2. Set AWS credentials in environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
3. Provide `db_password` as a variable (via -var or tfvars file)
4. From this folder run:

```bash
terraform init
terraform plan -var 'db_password=YOUR_PASSWORD'
terraform apply -var 'db_password=YOUR_PASSWORD'
```

Notes:
- This is a starting scaffold. You will likely want to add an ALB, ECS Task Definitions, and a CI/CD pipeline.
- State management: consider using remote state (S3 + DynamoDB) for team environments.
