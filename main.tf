resource "azurerm_resource_group" "resource_gp" {
  name     = "terraform-demo"
  location = "${var.location}"

  tags {
    Owner = "Angesh Vikram"
  }
}
