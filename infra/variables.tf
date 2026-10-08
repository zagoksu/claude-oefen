variable "name_prefix" {
  description = "Short prefix used to derive resource names (e.g. \"dplat01\"). Must be globally unique for the storage account and Key Vault."
  type        = string
  default     = "dplat01"
}

variable "location" {
  description = "Azure region to deploy resources into."
  type        = string
  default     = "westeurope"
}

variable "tags" {
  description = "Tags applied to all resources."
  type        = map(string)
  default = {
    project = "claude-oefen"
    env     = "practice"
  }
}
