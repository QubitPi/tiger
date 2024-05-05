packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "theresa-test-model-asr" {
  ami_name = "theresa-test-model-asr"
  force_deregister = "true"
  force_delete_snapshot = "true"

  region = "us-west-1"
  instance_type = "t2.large"
  launch_block_device_mappings {
    device_name           = "/dev/sda1"
    volume_size           = 60
    volume_type           = "gp2"
    delete_on_termination = true
  }

  source_ami_filter {
    filters = {
      name = "ubuntu/images/*ubuntu-*-22.04-amd64-server-*"
      root-device-type = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners = ["099720109477"]
  }
  ssh_username = "ubuntu"
}

build {
  name = "install-theresa-test-model-asr"
  sources = [
    "source.amazon-ebs.theresa-test-model-asr"
  ]

  # Load SSL Certificates into AMI image
  provisioner "file" {
    source = "fullchain.pem"
    destination = "/home/ubuntu/fullchain.pem"
  }
  provisioner "file" {
    source = "privkey.pem"
    destination = "/home/ubuntu/privkey.pem"
  }

  # Load Nginx config files into AMI image
  provisioner "file" {
    source = "nginx.conf"
    destination = "/home/ubuntu/nginx.conf"
  }
  provisioner "file" {
    source = "timeout.conf"
    destination = "/home/ubuntu/timeout.conf"
  }

  # Load flask app into AMI image
  provisioner "shell" {
    inline = [
      "mkdir -p /home/ubuntu/asr/"
    ]
  }
  provisioner "file" {
    source = "../../../test_models/asr/"
    destination = "/home/ubuntu/asr/"
  }

  provisioner "shell" {
    script = "setup.sh"
  }
}
