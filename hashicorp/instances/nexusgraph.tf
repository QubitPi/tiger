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

resource "aws_instance" "paion-data-nexusgraph-theresa-1" {
  ami = "${data.aws_ami.latest-nexusgraph-theresa.id}"
  instance_type = "t2.small"
  tags = {
    Name = "Paion Data nexusgraph Theresa 1"
  }
  security_groups = ["Paion Data nexusgraph Theresa"]

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

resource "aws_instance" "paion-data-nexusgraph-theresa-2" {
  ami = "${data.aws_ami.latest-nexusgraph-theresa.id}"
  instance_type = "t2.small"
  tags = {
    Name = "Paion Data nexusgraph Theresa 2"
  }
  security_groups = ["Paion Data nexusgraph Theresa"]

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

resource "aws_instance" "paion-data-nexusgraph-theresa-3" {
  ami = "${data.aws_ami.latest-nexusgraph-theresa.id}"
  instance_type = "t2.small"
  tags = {
    Name = "Paion Data nexusgraph Theresa 3"
  }
  security_groups = ["Paion Data nexusgraph Theresa"]

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
