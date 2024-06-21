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

data "aws_ami" "theresa-speech-recognition-flask" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["theresa-speech-recognition-flask"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "theresa-speech-recognition-flask" {
  ami = "${data.aws_ami.theresa-speech-recognition-flask.id}"
  instance_type = "t2.large"

  tags = {
    Name = "Theresa Speech Recognition Flask"
  }

  key_name = "testKey"
  security_groups = ["Theresa Speech Recognition Flask", "testKey SSH"]

  user_data = "${data.template_file.base-init.rendered}"
}
