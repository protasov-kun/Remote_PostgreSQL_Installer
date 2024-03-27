terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

locals {
  folder_id = "b1g27pnvvlliqavhq6d8"
  cloud_id  = "b1gh58hlo9our1iocsva"
}

// Configure the Yandex.Cloud provider
provider "yandex" {
  service_account_key_file = "${file("~/authorized_key.json")}"
  cloud_id                 = local.cloud_id
  folder_id                = local.folder_id
}
