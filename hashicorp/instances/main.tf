variable "aws_deploy_region" {
  type = string
  description = "The EC2 region"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.42.0"
    }
  }
  required_version = ">= 0.14.5"
}

provider "aws" {
  region = var.aws_deploy_region
}

data "aws_ami" "latest-theresa" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["theresa"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "theresa" {
  ami = "${data.aws_ami.latest-theresa.id}"
  instance_type = "t2.micro"
  key_name = "testKey"

  user_data = <<-EOF
    #!/bin/bash
    cd /home/ubuntu/theresa

    python3 -m venv .venv
    . .venv/bin/activate
    python3 -m pip install .
    export APP_CONFIG_FILE=/home/ubuntu/settings.cfg

    flask --app theresa run --host=0.0.0.0
  EOF
}
