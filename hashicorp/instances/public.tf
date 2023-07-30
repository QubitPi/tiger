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
  instance_type = "t2.small"
  tags = {
    Name = "Theresa Public"
  }
  security_groups = ["Theresa Public"]

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
