variable "name_prefix" {
  description = "Short prefix used to derive resource names (e.g. \"dplat01\")."
  type        = string
}

variable "location" {
  description = "Azure region to deploy resources into."
  type        = string
  default     = "westeurope"
}

variable "tags" {
  description = "Tags applied to all resources created by this module."
  type        = map(string)
  default     = {}
}
