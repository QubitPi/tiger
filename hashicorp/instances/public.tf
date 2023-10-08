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
  root_block_device {
    volume_size = 60
  }

  tags = {
    Name = "Theresa Public"
  }

  # key_name = "testKey"
  # security_groups = ["Theresa Public", "testKey SSH"]
  security_groups = ["Theresa Public"]

  user_data = <<-EOF
    #!/bin/bash
    alias python=python3.10
    alias python3=python3.10
    export APP_CONFIG_FILE=/home/ubuntu/settings.cfg

    sudo nginx -t
    sudo nginx -s reload

    cd /home/ubuntu/theresa
    gunicorn -w 4 -b 0.0.0.0 'theresa:create_app()'
  EOF
}
