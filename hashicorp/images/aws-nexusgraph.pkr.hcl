source "amazon-ebs" "nexusgraph-theresa" {
  ami_name = "nexusgraph-theresa"
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
  name = "install-nexusgraph-theresa"
  sources = [
    "source.amazon-ebs.nexusgraph-theresa"
  ]

  # Load Flask config file into AMI image
  provisioner "file" {
    source = "settings.cfg"
    destination = "/home/ubuntu/settings.cfg"
  }

  provisioner "shell" {
    environment_vars = [
      "GH_PAT_READ=${var.gh_pat_read}"
    ]
    script = "../scripts/nexusgraph-setup.sh"
  }
}
