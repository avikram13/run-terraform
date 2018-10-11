## Introduction

run-terraform is a python module provide a wrapper of `terraform` command line tool.
`terraform` is a tool made by Hashicorp, please refer to https://terraform.io/

## Prerequisites
###install python2.7.11 +
###Install the Azure CLI [https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest]
###Install the Terraform CLI [https://www.terraform.io/intro/getting-started/install.html]
###Install the python-terraform by running following cmd
  pip install python-terraform

## Usage
create a file config.json with following details

{
"subscription_id":<your_subscription_id>,
"client_secret":<your_client_secret>,
"location":<location> (example: "West US"),
"display_name":<display_name> (example: "av-demo"),
"homepage":<your homepage> (example: "http://av-demo-1"),
"identifier_uris":<your identifier_uris> (example: "http://av-demo-1.com"),
"role_assignment":<Role> (example:"Contributor"),
"tfvars":[
          {"subscription_id":""},
          {"tenant_id":""},
          {"client_id":""},
          {"client_secret":""},
          {"location":""}
        ]
}

copy foloowing files to your terraform directory and run cmd [python3 setup.py or python setup.py]
1) setup.py
2) main.tf
3) config.json
