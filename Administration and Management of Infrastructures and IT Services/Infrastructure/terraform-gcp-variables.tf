# How to define variables in terraform:
# https://www.terraform.io/docs/configuration/variables.html

# Name of the project, replace "XX" for your
# respective group ID
variable "GCP_PROJECT_ID" {
  default = "neural-cathode-365210"
}

# A list of machine types is found at:
# https://cloud.google.com/compute/docs/machine-types
# prices are defined per region, before choosing an instance
# check the cost at: https://cloud.google.com/compute/pricing#machinetype
# Minimum required is N1 type = "n1-standard-1, 1 vCPU, 3.75 GB RAM"
variable "GCP_MACHINE_TYPE" {
  default = "n1-standard-2"
}
variable "GCP_HEAVY_MACHINE_TYPE" {
  default = "n2-standard-4"
}

# Regions list is found at:
# https://cloud.google.com/compute/docs/regions-zones/regions-zones?hl=en_US
# For prices of your deployment check:
# Compute Engine dashboard -> VM instances -> Zone
variable "GCP_ZONE" {
  default = "europe-west2-c"
}

# Minimum required
variable "DISK_SIZE" {
  default = "15"
}

variable "zone_id" {
  default = "b0b4cd49dc51c9194b95df1bae07b8ee"
}

variable "domain" {
  default = "team-13.pt"
}
