source "amazon-ebs" "theresa-hanlp-ner" {
  ami_name = "theresa-hanlp-ner"
  force_deregister = "true"
  force_delete_snapshot = "true"
  skip_create_ami = "${var.skip_create_ami}"

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
  name = "install-theresa-hanlp-ner"
  sources = [
    "source.amazon-ebs.theresa-hanlp-ner"
  ]

  # Load Theresa executable
  provisioner "file" {
    source = "${var.theresa_tar_gz_path}"
    destination = "/home/ubuntu/theresa.tar.gz"
  }

  provisioner "shell" {
    scripts = [
      "../scripts/aws-theresa-hanlp-ner-setup.sh"
    ]
  }
}
