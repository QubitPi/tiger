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

data "aws_ami" "latest-theresa-dev" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["theresa-dev"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_ami" "latest-theresa-prod" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["theresa-prod"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "theresa-dev" {
  ami = "${data.aws_ami.latest-theresa-dev.id}"
  instance_type = "t2.micro"
  tags = {
    Name = "Paion Data Theresa (Dev)"
  }
  security_groups = ["Paion Data Theresa"]

  user_data = <<-EOF
    #!/bin/bash
    cd /home/ubuntu/theresa

    alias python=python3.10
    alias python3=python3.10

    python3.10 -m venv .venv
    . .venv/bin/activate
    python3.10 -m pip install .
    export APP_CONFIG_FILE=/home/ubuntu/settings.cfg

    sudo nginx -t
    sudo nginx -s reload

    flask --app theresa run --host=0.0.0.0
  EOF
}

resource "aws_route53_record" "machine-learning-paion-data-dev" {
  zone_id         = "Z02600613NNEBWDLMOCCJ"
  name            = "machine-learning.paion-data.dev"
  type            = "A"
  ttl             = 300
  records         = [aws_instance.theresa-dev.public_ip]
  allow_overwrite = true
}

resource "aws_instance" "theresa-prod" {
  ami = "${data.aws_ami.latest-theresa-prod.id}"
  instance_type = "t2.small"
  tags = {
    Name = "Paion Data Theresa (Prod)"
  }
  security_groups = ["Paion Data Theresa"]

  user_data = <<-EOF
    #!/bin/bash
    cd /home/ubuntu/theresa

    alias python=python3.10
    alias python3=python3.10

    python3.10 -m venv .venv
    . .venv/bin/activate
    python3.10 -m pip install .
    export APP_CONFIG_FILE=/home/ubuntu/settings.cfg

    sudo nginx -t
    sudo nginx -s reload

    flask --app theresa run --host=0.0.0.0
  EOF
}

resource "aws_route53_record" "machine-learning-paion-data-com" {
  zone_id         = "Z041761836EZCKFO9AWXN"
  name            = "machine-learning.paion-data.com"
  type            = "A"
  ttl             = 300
  records         = [aws_instance.theresa-prod.public_ip]
  allow_overwrite = true
}
