output "container_name" {
  value = var.name
}

output "ssh_command" {
  value       = "ssh -p ${var.host_ssh_port} ${var.ssh_user}@127.0.0.1"
  description = "SSH into container via forwarded port on host"
}

output "http_url" {
  value       = "http://<SERVER_PUBLIC_IP>:${var.host_http_port}"
  description = "HTTP forwarded to container"
}

output "app_url" {
  value       = "http://<SERVER_PUBLIC_IP>:${var.host_app_port}"
  description = "Port 5000 forwarded to container"
}
