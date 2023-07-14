Deployment Documentation
------------------------

Theresa has been deployed to

- **machine-learning.paion-data.dev**: single EC2 instance with dedicated SSL certificate for internal Paion Data development team
- **machine-learning.paion-data.com**: single EC2 instance with dedicated SSL certificate serving
  [Theresa Rapid API](https://rapidapi.com/paion-data-machine-learning/api/theresa3)
- **3 EC2 instances without certificates behind load balancer**: serving app.nexusgraph.com production environment

### AMI Images (HashiCorp Packer)

- All images share the same [Flask config file](./images/settings.cfg),
  [variable declaration file](./images/variables.pkr.hcl), and [variable value file](./images/theresa.auto.pkrvars.hcl)
- [aws-theresa.pkr.hcl](./images/aws-theresa.pkr.hcl) builds image for `machine-learning.paion-data.dev` and `machine-learning.paion-data.com`

  - `machine-learning.paion-data.dev` uses [dev Nginx config file](./images/nginx-ssl-dev.conf)
  - `machine-learning.paion-data.com` uses [prod Nginx config file](./images/nginx-ssl-prod.conf)

- [aws-nexusgraph.pkr.hcl](./images/aws-nexusgraph.pkr.hcl) builds images for nexusgraph.com

### EC2 Instances (HashiCorp Terraform)

- [main.tf](./instances/main.tf) deploys instances for `machine-learning.paion-data.dev` and `machine-learning.paion-data.com`
- [nexusgraph.tf](./instances/nexusgraph.tf) deploy instances for nexusgraph.com
