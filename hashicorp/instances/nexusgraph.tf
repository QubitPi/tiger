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
  instance_type = "t2.small"
  tags = {
    Name = "Paion Data Nexus Graph Theresa"
  }
  security_groups = ["Paion Data Nexus Graph Theresa"]

  user_data = <<-EOF
    #!/bin/bash
    cd /home/ubuntu/theresa

    alias python=python3.10
    alias python3=python3.10

    python3.10 -m venv .venv
    . .venv/bin/activate
    python3.10 -m pip install .
    export APP_CONFIG_FILE=/home/ubuntu/settings.cfg

    gunicorn -w 4 -b 0.0.0.0 'theresa:create_app()'
  EOF
}

resource "aws_route53_record" "theresa-nexusgraph-com" {
  zone_id         = var.nexusgraph_zone_id
  name            = "theresa.nexusgraph.com"
  type            = "A"
  ttl             = 300
  records         = [aws_instance.paion-data-nexusgraph-theresa.public_ip]
  allow_overwrite = true
}
