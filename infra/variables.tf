variable "aws_region" {
    type = string
    default = "us-east-2"
}

variable "app_name" {
    type = string
    default = "ai-tutor"
}

variable "db_name" {
    type = string
    default = "ai-tutor"
}

variable "db_username" {
    type = string
    default = "admin"
}

variable "db_password" {
    type = string
    default = "loophole@123"
}


variable "container_image" {
    description = "Docker image for AI Tutor backend"
    type        = string
    default = "your-dockerhub-username/ai-tutor:latest"
}


variable "container_port" {
  type    = number
  default = 8000
}

variable "database_url" {
    type = string
    sensitive = true
}

variable "admin_api_key" {
    type = string
    sensitive = true
}

variable "backend_image" {
  description = "Docker image for AI Tutor backend"
  type        = string
}
