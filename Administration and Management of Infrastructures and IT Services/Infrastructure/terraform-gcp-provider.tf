# Terraform google cloud multi tier deployment

# check how configure the provider here:
# https://www.terraform.io/docs/providers/google/index.html
provider "google" {
  # Create/Download your credentials from:
  # Google Console -> "APIs & services -> Credentials"
  # Choose create- > "service account key" -> compute engine service account -> JSON
  credentials = file("neural-cathode-365210-d7f4e5203bcd.json")
  project     = var.GCP_PROJECT_ID
  zone        = var.GCP_ZONE
}

provider "cloudflare" {
  api_token = "nkQowS3oTNg4wb6eXrFnp4cwXUMlADU69Ow_3gVY"
}
