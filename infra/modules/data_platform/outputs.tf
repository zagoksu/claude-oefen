output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "storage_account_name" {
  value = azurerm_storage_account.datalake.name
}

output "storage_account_id" {
  value = azurerm_storage_account.datalake.id
}

output "filesystem_name" {
  value = azurerm_storage_data_lake_gen2_filesystem.raw.name
}

output "key_vault_name" {
  value = azurerm_key_vault.this.name
}

output "key_vault_uri" {
  value = azurerm_key_vault.this.vault_uri
}
