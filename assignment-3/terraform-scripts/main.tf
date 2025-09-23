terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

# ----------------------------
# VPC
# ----------------------------
data "aws_availability_zones" "available" {}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.21"

  name = "ci-cd-vpc"
  cidr = "10.0.0.0/16"

  azs             = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Terraform   = "true"
    Environment = var.environment
  }
}

// ECS cluster: use native resource because module doesn't accept cluster_configuration/vpc/subnets
resource "aws_ecs_cluster" "this" {
  name = "ci-cd-ecs"

  configuration {
    execute_command_configuration {
      logging = "OVERRIDE"
    }
  }

  tags = {
    Environment = var.environment
  }
}


# ----------------------------
# Security Groups
# ----------------------------
resource "aws_security_group" "ecs_tasks" {
  name        = "ecs-tasks-sg"
  vpc_id      = module.vpc.vpc_id
  description = "Security group for ECS tasks"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = var.environment
  }
}

resource "aws_security_group" "rds" {
  name        = "rds-sg"
  vpc_id      = module.vpc.vpc_id
  description = "Allow ECS tasks to access RDS"

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = var.environment
  }
}

# ----------------------------
# RDS Subnet Group
# ----------------------------
resource "aws_db_subnet_group" "rds_subnet" {
  name       = "rds-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "rds-subnet-group"
  }
}

# ----------------------------
# RDS Instance
# ----------------------------
resource "aws_db_instance" "postgres" {
  identifier        = "ci-cd-postgres"
  engine            = "postgres"
  engine_version    = var.rds_engine_version
  instance_class    = var.rds_instance_class
  allocated_storage = var.rds_allocated_storage

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  skip_final_snapshot    = true
  publicly_accessible    = false
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  storage_encrypted = true

  tags = {
    Environment = var.environment
  }
}
