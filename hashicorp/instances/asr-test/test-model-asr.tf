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
  region = "us-west-1"
}

data "template_file" "base-init" {
  template = "${file("start.sh")}"
}

data "aws_ami" "theresa-test-model-asr" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["theresa-test-model-asr"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "theresa-test-model-asr" {
  ami = "${data.aws_ami.theresa-test-model-asr.id}"
  instance_type = "t2.large"

  tags = {
    Name = "Paion Data Dev ASR"
  }

  key_name = "testKey"
  security_groups = ["Paion Data Dev ASR", "testKey SSH"]

  user_data = "${data.template_file.base-init.rendered}"
}

resource "aws_route53_record" "theresa-test-model-asr" {
  zone_id         = "Z02600613NNEBWDLMOCCJ"
  name            = "asr-test.paion-data.dev"
  type            = "A"
  ttl             = 300
  records         = [aws_instance.theresa-test-model-asr.public_ip]
  allow_overwrite = true
}
