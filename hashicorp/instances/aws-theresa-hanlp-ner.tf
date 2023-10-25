data "template_file" "base-init" {
  template = "${file("../scripts/aws-theresa-hanlp-ner-tf-init.sh")}"
}

data "aws_ami" "latest-theresa-hanlp-ner" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["theresa-hanlp-ner"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "theresa-hanlp-ner" {
  ami = "${data.aws_ami.latest-theresa-hanlp-ner.id}"
  instance_type = "t2.large"

  tags = {
    Name = "Theresa HanLP NER"
  }

  key_name = "testKey"
  security_groups = ["Theresa HanLP NER", "testKey SSH"]

  user_data = "${data.template_file.base-init.rendered}"
}
