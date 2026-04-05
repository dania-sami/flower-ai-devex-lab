terraform {
  required_version = ">= 1.5.0"
}

variable "project_name" {
  type    = string
  default = "flower-platform-data-lab"
}

output "project_name" {
  value = var.project_name
}
