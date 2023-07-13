Deployment Documentation
------------------------

Theresa has been deployed to

- **machine-learning.paion-data.dev** (single EC2 instance with dedicated SSL certificate): dev instance to paion-data development team
- **machine-learning.paion-data.com** (single EC2 instance with dedicated SSL certificate): serving
  [Theresa Rapid API](https://rapidapi.com/paion-data-machine-learning/api/theresa3)
- **3 EC2 instances without certificates behind load balancer**: serving app.nexusgraph.com production environment
