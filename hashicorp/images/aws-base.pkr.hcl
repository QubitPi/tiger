variable "aws_image_region" {
  type =  string
  sensitive = true
}

variable "theresa_settings_config_path" {
  type =  string
  sensitive = true
}

variable "theresa_tar_gz_path" {
  type =  string
  sensitive = true
}

variable "skip_create_ami" {
  type =  bool
  sensitive = true
}

packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}
