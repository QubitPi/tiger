packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "theresa" {
  ami_name = "theresa"
  force_deregister = "true"
  force_delete_snapshot = "true"

  instance_type = "t2.small"
  region = "${var.aws_image_region}"
  source_ami_filter {
    filters = {
      name = "ubuntu/images/*ubuntu-*-20.04-amd64-server-*"
      root-device-type = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners = ["099720109477"]
  }
  ssh_username = "ubuntu"
}

build {
  name = "install-theresa"
  sources = [
    "source.amazon-ebs.theresa"
  ]

  # Load Flask config file into AMI image
  provisioner "file" {
    source = "settings.cfg"
    destination = "/home/ubuntu/settings.cfg"
  }

  # Load SSL Certificates into AMI image
  provisioner "file" {
    source = "./server.crt"
    destination = "/home/ubuntu/server.crt"
  }
  provisioner "file" {
    source = "./server.key"
    destination = "/home/ubuntu/server.key"
  }

  # Load Nginx config file into AMI image
  provisioner "file" {
    source = "./nginx-ssl.conf"
    destination = "/home/ubuntu/nginx-ssl.conf"
  }

  provisioner "shell" {
    environment_vars = [
      "GH_PAT_READ=${var.gh_pat_read}"
    ]
    script = "../scripts/setup.sh"
  }
}
