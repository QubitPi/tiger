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

    gunicorn -w 4 -b 0.0.0.0 'theresa:create_app()'
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
