Deployment Documentation
------------------------

Theresa has been deployed to

- **machine-learning.paion-data.dev** (single EC2 instance with dedicated SSL certificate): dev instance to paion-data development team
- **machine-learning.paion-data.com** (single EC2 instance with dedicated SSL certificate): serving
  [Theresa Rapid API](https://rapidapi.com/paion-data-machine-learning/api/theresa3)
- **3 EC2 instances without certificates behind load balancer**: serving app.nexusgraph.com production environment

The following GitHub Secrets needs to be defined:

- GH_PAT_READ

- AWS
- AWS_ACCESS_KEY_ID
- AWS_REGION
- AWS_SECRET_ACCESS_KEY

- SSL_CERTIFICATE_DEV
- SSL_CERTIFICATE_KEY_DEV
- SSL_CERTIFICATE_KEY_PROD
- SSL_CERTIFICATE_PROD

- OPEN_AI_API_KEY

- GOOGLE_KNOWLEDGE_GRAPH_API_KEY

- X_RAPIDAPI_KEY_MICROSOFT_ENTITY_EXTRACTION
- X_RAPIDAPI_KEY_MICROSOFT_LANGUAGE_DETECTION
