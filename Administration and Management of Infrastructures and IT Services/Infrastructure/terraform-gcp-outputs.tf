# Terraform GCP
# To output variables, follow pattern:
# value = TYPE.NAME.ATTR

output "database" {
  value = join(" ", google_compute_instance.db.*.network_interface.0.access_config.0.nat_ip)
}

output "balancer" {
  value = join(" ", google_compute_instance.balancer.*.network_interface.0.access_config.0.nat_ip)
}

output "balancer_ssh" {
  value = google_compute_instance.balancer.self_link
}

# example for a set of identical instances created with "count"
output "web_frontend" {
  value = formatlist("%s = %s", google_compute_instance.web-front[*].name, google_compute_instance.web-front[*].network_interface.0.access_config.0.nat_ip)
}

output "web_backend" {
  value = formatlist("%s = %s", google_compute_instance.web-back[*].name, google_compute_instance.web-back[*].network_interface.0.access_config.0.nat_ip)
}