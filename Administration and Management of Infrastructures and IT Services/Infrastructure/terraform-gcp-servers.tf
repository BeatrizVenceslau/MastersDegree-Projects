
# Elemets of the cloud such as virtual servers,
# networks, firewall rules are created as resources
# syntax is: resource RESOURCE_TYPE RESOURCE_NAME
# https://www.terraform.io/docs/configuration/resources.html

###########  Web Servers   #############
# This method creates as many identical instances as the "count" index value
resource "google_compute_instance" "web-front" {
  count        = 2
  name         = "front${count.index + 1}"
  machine_type = var.GCP_MACHINE_TYPE
  zone         = var.GCP_ZONE

  boot_disk {
    initialize_params {
      # image list can be found at:
      # https://cloud.google.com/compute/docs/images
      image = "ubuntu-2004-focal-v20220927"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata = {
    ssh-keys = "ubuntu:${file("./id_rsa.pub")}"
  }
  tags = ["web-front"]
}

resource "google_compute_instance" "web-back" {
  count        = 2
  name         = "back${count.index + 1}"
  machine_type = var.GCP_MACHINE_TYPE
  zone         = var.GCP_ZONE

  boot_disk {
    initialize_params {
      # image list can be found at:
      # https://cloud.google.com/compute/docs/images
      image = "ubuntu-2004-focal-v20220927"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata = {
    ssh-keys = "ubuntu:${file("./id_rsa.pub")}"
  }
  tags = ["web-back"]
}


###########  Load Balancer   #############
resource "google_compute_instance" "balancer" {
  name         = "balancer"
  machine_type = var.GCP_MACHINE_TYPE
  zone         = var.GCP_ZONE

  boot_disk {
    initialize_params {
      # image list can be found at:
      # https://cloud.google.com/compute/docs/images
      image = "ubuntu-2004-focal-v20220927"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata = {
    ssh-keys = "ubuntu:${file("./id_rsa.pub")}"
  }

  tags = ["balancer"]
}


###########  Databases   #############
resource "google_compute_instance" "db" {
  name         = "db"
  machine_type = var.GCP_MACHINE_TYPE
  zone         = var.GCP_ZONE

  boot_disk {
    initialize_params {
      # image list can be found at:
      # https://cloud.google.com/compute/docs/images
      image = "ubuntu-2004-focal-v20220927"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata = {
    ssh-keys = "ubuntu:${file("./id_rsa.pub")}"
  }

  tags = ["db"]
}

###########  Monitoring   #############
resource "google_compute_instance" "monitoring" {
  name         = "mon"
  machine_type = var.GCP_HEAVY_MACHINE_TYPE
  zone         = var.GCP_ZONE

  boot_disk {
    initialize_params {
      # image list can be found at:
      # https://cloud.google.com/compute/docs/images
      image = "ubuntu-2004-focal-v20220927"
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  metadata = {
    ssh-keys = "ubuntu:${file("./id_rsa.pub")}"
  }

  tags = ["monitoring"]
}

data "template_file" "ansible_hosts" {
  template = templatefile("${path.module}/hosts.tmpl",
    {
      hosts = {
        front1   = google_compute_instance.web-front[0].network_interface[0].access_config[0].nat_ip
        front2   = google_compute_instance.web-front[1].network_interface[0].access_config[0].nat_ip
        back1    = google_compute_instance.web-back[0].network_interface[0].access_config[0].nat_ip
        back2    = google_compute_instance.web-back[1].network_interface[0].access_config[0].nat_ip
        balancer = google_compute_instance.balancer.network_interface[0].access_config[0].nat_ip
        db       = google_compute_instance.db.network_interface[0].access_config[0].nat_ip
        mon      = google_compute_instance.monitoring.network_interface[0].access_config[0].nat_ip
      },
      web-hosts-front = {
        front1 = google_compute_instance.web-front[0].network_interface[0].access_config[0].nat_ip
        front2 = google_compute_instance.web-front[1].network_interface[0].access_config[0].nat_ip
      },
      web-hosts-back = {
        back1 = google_compute_instance.web-back[0].network_interface[0].access_config[0].nat_ip
        back2 = google_compute_instance.web-back[1].network_interface[0].access_config[0].nat_ip
      }
  })
}

resource "cloudflare_record" "web-front-dsn" {
  depends_on = [
    google_compute_instance.web-front
  ]
  count   = length(google_compute_instance.web-front)
  zone_id = var.zone_id
  name    = google_compute_instance.web-front[count.index].name
  value   = google_compute_instance.web-front[count.index].network_interface[0].access_config[0].nat_ip
  type    = "A"
  ttl     = 1
  proxied = false
}
resource "cloudflare_record" "web-back-dsn" {
  depends_on = [
    google_compute_instance.web-back
  ]
  count   = length(google_compute_instance.web-back)
  zone_id = var.zone_id
  name    = google_compute_instance.web-back[count.index].name
  value   = google_compute_instance.web-back[count.index].network_interface[0].access_config[0].nat_ip
  type    = "A"
  ttl     = 1
  proxied = false
}
resource "cloudflare_record" "db-dsn" {
  depends_on = [
    google_compute_instance.db
  ]
  //count   = length(google_compute_instance.db)
  zone_id = var.zone_id
  name    = "db"
  value   = google_compute_instance.db.network_interface[0].access_config[0].nat_ip
  type    = "A"
  ttl     = 1
  proxied = false
}
resource "cloudflare_record" "balancer-dsn" {
  depends_on = [
    google_compute_instance.balancer
  ]
  //count   = length(google_compute_instance.balancer)
  zone_id = var.zone_id
  name    = "balancer"
  value   = google_compute_instance.balancer.network_interface[0].access_config[0].nat_ip
  type    = "A"
  ttl     = 1
  proxied = false
}
resource "cloudflare_record" "monitoring-dsn" {
  depends_on = [
    google_compute_instance.monitoring
  ]
  //count   = length(google_compute_instance.monitoring)
  zone_id = var.zone_id
  name    = "monitoring"
  value   = google_compute_instance.monitoring.network_interface[0].access_config[0].nat_ip
  type    = "A"
  ttl     = 1
  proxied = false
}

resource "null_resource" "prepare-provision-machines" {
  depends_on = [
    google_compute_instance.web-front,
    google_compute_instance.web-back,
    google_compute_instance.balancer,
    google_compute_instance.db,
    google_compute_instance.monitoring,
    data.template_file.ansible_hosts
  ]

  provisioner "local-exec" {
    command = "cat > ../Provisioner/gcphosts <<EOL\n${join("", data.template_file.ansible_hosts.*.rendered)}\nEOL"
  }
  provisioner "local-exec" {
    command = "cat  ../Provisioner/gcphosts"
  }
}
