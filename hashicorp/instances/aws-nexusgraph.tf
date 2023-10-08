variable "nexusgraph_zone_id" {
  type = string
  description = "Hosted zone ID on Route 53"
  sensitive = true
}

data "aws_ami" "latest-nexusgraph-theresa" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["nexusgraph-theresa"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "paion-data-nexusgraph-theresa" {
  ami = "${data.aws_ami.latest-nexusgraph-theresa.id}"
  instance_type = "t2.large"

  tags = {
    Name = "Paion Data Nexus Graph Theresa"
  }

  key_name = "testKey"
  security_groups = ["Paion Data Nexus Graph Theresa", "testKey SSH"]

  user_data = "${data.template_file.base-init.rendered}"
}

resource "aws_route53_record" "theresa-nexusgraph-com" {
  zone_id         = var.nexusgraph_zone_id
  name            = "theresa.nexusgraph.com"
  type            = "A"
  ttl             = 300
  records         = [aws_instance.paion-data-nexusgraph-theresa.public_ip]
  allow_overwrite = true
}
