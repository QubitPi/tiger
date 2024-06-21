packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "theresa-speech-recognition-flask" {
  ami_name = "theresa-speech-recognition-flask"
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
  sources = [
    "source.amazon-ebs.theresa-speech-recognition-flask"
  ]

  # Load flask app into AMI image
  provisioner "shell" {
    inline = [
      "mkdir -p /home/ubuntu/speechrecognition/"
    ]
  }
  provisioner "file" {
    source = "../../../speechrecognition/"
    destination = "/home/ubuntu/speechrecognition/"
  }

  provisioner "shell" {
    script = "setup.sh"
  }
}
