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

  instance_type = "t2.micro"
  region = "us-west-1"
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

  # Load Flas config file into AMI image
  # path is "/home/ubuntu/settings.cfg"
  provisioner "file" {
    source = "settings.cfg"
    destination = "/home/ubuntu"
  }

  provisioner "shell" {
    environment_vars = [
      "GH_PAT_READ=${var.gh_pat_read}"
    ]
    script = "../scripts/setup.sh"
  }
}
