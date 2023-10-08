data "aws_ami" "latest-theresa-public" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["theresa-public"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "theresa-public" {
  ami = "${data.aws_ami.latest-theresa-public.id}"
  instance_type = "t2.large"

  tags = {
    Name = "Theresa Public"
  }

  key_name = "testKey"
  security_groups = ["Theresa Public", "testKey SSH"]

  user_data = "${data.template_file.base-init.rendered}"
}
