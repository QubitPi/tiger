variable "aws_deploy_region" {
  type = string
  description = "The EC2 region"
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.42.0"
    }
#    acme = {
#      source  = "vancluever/acme"
#      version = "~> 2.0"
#    }
  }
  required_version = ">= 0.14.5"
}

provider "aws" {
  region = var.aws_deploy_region
}

data "aws_ami" "latest-theresa" {
  most_recent = true
  owners = ["899075777617"]

  filter {
    name   = "name"
    values = ["theresa"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "theresa" {
  ami = "${data.aws_ami.latest-theresa.id}"
  instance_type = "t2.small"
  tags = {
    Name = "Theresa"
  }
  key_name = "testKey"
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

    flask --app theresa run --host=0.0.0.0
  EOF
}

# Do NOT use this resource. It creates new domain at every execution
#resource "aws_route53_zone" "primary" {
#  name = "externalbrain.app"
#}


resource "aws_route53_record" "machine-learning-paion-data-com" {
  zone_id         = "Z041761836EZCKFO9AWXN"
  name            = "machine-learning.paion-data.com"
  type            = "A"
  ttl             = 300
  records         = [aws_instance.theresa.public_ip]
  allow_overwrite = true
}
#
#provider "acme" {
#  server_url = "https://acme-v02.api.letsencrypt.org/directory"
#}
#
#data "aws_route53_zone" "base_domain" {
#  name = "externalbrain.app"
#}
#
#resource "tls_private_key" "private_key" {
#  algorithm = "RSA"
#}
#
#resource "acme_registration" "registration" {
#  account_key_pem = tls_private_key.private_key.private_key_pem
#  email_address   = "jack20220723@gmail.com"
#
#  depends_on = [aws_route53_record.machine-learning-externalbrain]
#}
#
#resource "acme_certificate" "certificate" {
#  account_key_pem           = acme_registration.registration.account_key_pem
#  common_name               = data.aws_route53_zone.base_domain.name
#  subject_alternative_names = ["*.${data.aws_route53_zone.base_domain.name}"]
#
#  dns_challenge {
#    provider = "route53"
#
#    config = {
#      AWS_HOSTED_ZONE_ID = data.aws_route53_zone.base_domain.zone_id
#    }
#  }
#
#  depends_on = [acme_registration.registration]
#}






#resource "aws_acm_certificate" "certificate" {
#  certificate_body  = acme_certificate.certificate.certificate_pem
#  private_key       = acme_certificate.certificate.private_key_pem
#  certificate_chain = acme_certificate.certificate.issuer_pem
#
#  depends_on = [acme_certificate.certificate]
#}







#resource "local_file" "ssl-certificate" {
#  content  = acme_certificate.certificate.certificate_pem
#  filename = "/home/ubuntu/server.crt"
#
#  depends_on = [aws_acm_certificate.certificate]
#}
#
#resource "local_file" "ssl-certificate-key" {
#  content  = acme_certificate.certificate.private_key_pem
#  filename = "/home/ubuntu/server.key"
#
#  depends_on = [aws_acm_certificate.certificate]
#}

#resource "null_resource" "theresa" {
#
#  provisioner "remote-exec" {
#    inline = [
#      "sudo echo '${acme_certificate.certificate.certificate_pem}' > /etc/ssl/certs/server.crt",
#      "sudo echo '${acme_certificate.certificate.private_key_pem}' >  /etc/ssl/private/server.key",
##      "sudo mv /home/ubuntu/server.crt /etc/ssl/certs/server.crt",
##      "sudo mv /home/ubuntu/server.key /etc/ssl/private/server.key",
#      "sudo nginx -t && sudo nginx -s reload"
#    ]
#  }
#
#  depends_on = [aws_acm_certificate.certificate]
#}
