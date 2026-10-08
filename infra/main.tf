module "data_platform" {
  source = "./modules/data_platform"

  name_prefix = var.name_prefix
  location    = var.location
  tags        = var.tags
}
