terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }

  # No backend block: state is kept local on purpose for this practice project.
}

provider "azurerm" {
  features {}
}
