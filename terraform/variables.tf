variable "name" {
  description = "LXD container name"
  type        = string
  default     = "lab04-tf"
}

variable "image" {
  description = "LXD image alias"
  type        = string
  default     = "ubuntu:24.04"
}

variable "ssh_user" {
  description = "User inside container"
  type        = string
  default     = "ubuntu"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key on the server"
  type        = string
}

variable "host_ssh_port" {
  description = "Host port forwarded to container 22"
  type        = number
  default     = 2222
}

variable "host_http_port" {
  description = "Host port forwarded to container 80"
  type        = number
  default     = 8080
}

variable "host_app_port" {
  description = "Host port forwarded to container 5000"
  type        = number
  default     = 5000
}
