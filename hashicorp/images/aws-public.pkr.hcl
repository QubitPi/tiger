source "amazon-ebs" "theresa-public" {
  ami_name = "theresa-public"
  force_deregister = "true"
  force_delete_snapshot = "true"

  instance_type = "t2.large"
  launch_block_device_mappings {
    device_name = "/dev/sda1"
    volume_size = 60
    volume_type = "gp2"
    delete_on_termination = false
  }

  region = "${var.aws_image_region}"
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
  name = "install-theresa-public"
  sources = [
    "source.amazon-ebs.theresa-public"
  ]

  # Load Flask config file into AMI image
  provisioner "file" {
    source = "settings.cfg"
    destination = "/home/ubuntu/settings.cfg"
  }

  # Load Nginx config file into AMI image
  provisioner "file" {
    source = "./nginx-public.conf"
    destination = "/home/ubuntu/nginx.conf"
  }

  # Load Theresa executable
  provisioner "file" {
    source = "./theresa.tar.gz"
    destination = "/home/ubuntu/theresa.tar.gz"
  }

  provisioner "shell" {
    script = "../scripts/base-setup.sh"
  }
}
