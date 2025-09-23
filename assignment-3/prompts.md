# Prompts for working with assignment-3 infra and deployment

This file collects useful prompts you can reuse when iterating on the infrastructure we set up in Terraform (VPC, ECS Cluster, RDS) and when debugging or extending it.

---

## 1) VPC Setup
- "Write a Terraform module that provisions a VPC with CIDR 10.0.0.0/16, public and private subnets, NAT gateway, and internet gateway. Ensure it uses `terraform-aws-modules/vpc/aws`."
- "Add Terraform outputs for VPC ID, private subnets, and public subnets."

---

## 2) ECS Cluster
- "Create an ECS cluster using `terraform-aws-modules/ecs/aws`. Name should be configurable by a variable. Enable container insights."
- "Add Terraform outputs to expose ECS cluster name and ID."

---

## 3) Security Groups
- "Write Terraform security groups so ECS tasks can connect to RDS on port 5432. Allow ECS tasks all egress, and restrict RDS ingress to only ECS security group."
- "Update RDS to use the RDS security group instead of the default VPC security group."

---

## 4) RDS Setup
- "Provision an RDS Postgres instance in private subnets using Terraform. Use `aws_db_subnet_group` for private subnets and `aws_db_instance` for the database. Disable public accessibility. Enable storage encryption."
- "Use variables for DB name, username, password, engine version, instance class, and storage."
- "Add Terraform outputs for RDS endpoint, DB name, and username."

---

## 5) Variables and Outputs
- "Define Terraform variables for aws_region, environment, rds_engine_version, rds_instance_class, rds_allocated_storage, db_name, db_username, and db_password."
- "Mark db_password as sensitive in variables.tf."
- "Expose RDS endpoint, VPC ID, subnet IDs, and ECS cluster name in outputs.tf."

---

## 6) Troubleshooting
- "Terraform apply fails with `SubnetGroupNotFound` when creating the RDS instance. Explain probable causes and which Terraform resources to inspect."
- "ECS cluster is created but I cannot run services. Explain what additional resources are needed to deploy tasks in ECS (task definition, service, IAM roles, networking)."
- "RDS is unreachable from ECS tasks. List the security group and subnet configurations to check."

---

## 7) Cost and Cleanup
- "Tag all Terraform resources with `Environment` and `Owner`. Show how to enforce this with default_tags in the provider block."
- "Provide a safe cleanup command (terraform destroy) and explain how to confirm resource deletion."

---

Keep these prompts handy and adapt them when extending the infra with services like ALB, ECS tasks, or CI/CD pipelines.
