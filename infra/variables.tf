variable "aws_region" {
  type    = string
  default = "us-east-2"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "app_name" {
  type    = string
  default = "ai-tutor"
}

variable "db_name" {
  type    = string
  default = "aitutor"
  validation {
    condition     = can(regex("^[A-Za-z][A-Za-z0-9]*$", var.db_name))
    error_message = "db_name must begin with a letter and contain only alphanumeric characters."
  }
}

variable "db_username" {
  type    = string
  default = "aiadmin"
  validation {
    condition     = can(regex("^[A-Za-z][A-Za-z0-9_]*$", var.db_username)) && lower(var.db_username) != "admin"
    error_message = "db_username must start with a letter, contain only alphanumerics/underscore, and cannot be 'admin'."
  }
}

variable "db_password" {
  type    = string
  default = "loophole123!"
  validation {
    condition     = can(regex("^[\\x21-\\x7E]+$", var.db_password)) && !can(regex("[/@\\\" ]", var.db_password))
    error_message = "db_password must be printable ASCII and cannot contain '/', '@', '\"', or spaces."
  }
}


variable "container_image" {
  description = "Docker image for AI Tutor backend"
  type        = string
  default     = "your-dockerhub-username/ai-tutor:latest"
}


variable "container_port" {
  type    = number
  default = 8000
}



variable "admin_api_key" {
  type      = string
  sensitive = true
}

variable "backend_image" {
  description = "Docker image for AI Tutor backend"
  type        = string
}

variable "db_instance_type" {
  description = "RDS instance type"
  type        = string
  default     = "db.t3.micro"
}

variable "ecs_cpu" {
  description = "ECS task CPU units"
  type        = number
  default     = 512
}

variable "ecs_memory" {
  description = "ECS task memory in MiB"
  type        = number
  default     = 1024
}


variable "ui_bucket_name" {
  description = "S3 bucket name for UI"
  type        = string
}

variable "ui_domain_name" {
  description = "Optional custom domain (leave empty for now)"
  type        = string
  default     = ""
}