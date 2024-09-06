
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.116.0"
    }
  }
  required_version = ">=1.4"
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

data "azurerm_app_service" "app_service" {
  name                = "skynetflaskappdev"   # Replace with your App Service name
  resource_group_name = "skynet"     # Replace with your App Service resource group
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

  subscription_required    = true
  revision_description = "Initial API version"

}

resource "azurerm_api_management_backend" "apim_backend" {
  name                = "skynetflaskAPIbackend"
  api_management_name = "skynetapimdev"
  resource_group_name = "skynet"
  url                 = "https://${data.azurerm_app_service.app_service.default_site_hostname}"
  protocol = "http" # or "https" if your App Service supports it
}

resource "azurerm_api_management_api_policy" "api_policy" {
  api_name            = azurerm_api_management_api.skynet_api.name
  api_management_name = azurerm_api_management_api.skynet_api.api_management_name
  resource_group_name = azurerm_api_management_api.skynet_api.resource_group_name

  xml_content = <<XML
<policies>
  <inbound>
    <base />
    <set-backend-service base-url="https://${data.azurerm_app_service.app_service.default_site_hostname}" />
  </inbound>
  <backend>
    <base />
  </backend>
  <outbound>
    <base />
  </outbound>
  <on-error>
    <base />
  </on-error>
</policies>
XML
}