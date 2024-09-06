
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.101.0"
    }
  }
  required_version = ">=1.4"
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

# Import the API into API Management
resource "azurerm_api_management_api" "skynet_api" {
  name                = "skynetflaskapi"  # API ID
  resource_group_name = "skynet"
  api_management_name = "skynetapimdev"
  revision            = "v1"  # API revision
  display_name        = "Skynet Flask API"  # Display name of the API
  path                = ""  # Path for the API
  protocols           = ["http"]

  # Reference the OpenAPI specification file from the root folder
  import {
    content_format = "openapi"  # OpenAPI specification format
    content_value  = file("${path.module}/../swagger.json")  # Path to the swagger.json file
  }
}