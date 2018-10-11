#!/bin/python

#enter = int(input('Enter number of instances: '))

import subprocess
import json
import time
import os

answer = input('Want to run only Terraform script without creating .tfvars file: Enter Y for yes')

if answer.lower() not in ['y', 'yes']:

    # Install and Configure the Azure CLI
    command = 'az cloud set --name AzureCloud'
    output = subprocess.check_call(command.split())

    exists = os.path.isfile('config.json')
    if exists == False:
        print("kindly create config.json file to run this script")
        exit()

    with open('config.json') as f:
        config_data = json.load(f)
    print(config_data)

    #init Value

    # tenant Id
    tenant_id = ""

    # subscription Id
    subscription_id = config_data["subscription_id"]

    client_id = ""

    # client_secret
    client_secret = config_data["client_secret"]
    location = config_data["location"]

    # Set Your Default Subscription
    command = 'az account set --subscription ' + subscription_id
    output = subprocess.check_call(command.split())

    # account List
    command = 'az account list'
    output = subprocess.check_output(command.split())
    az_list = json.loads(output)

    for az_obj in az_list:
        if az_obj["isDefault"]:
            tenant_id = az_obj["tenantId"]
            subscription_id = az_obj["id"]
    if tenant_id == "":
        exit()

    print(tenant_id)
    print(subscription_id)

    # Create an Azure Active Directory (AAD) Application
    exists = os.path.isfile('createAAD.json')
    createAADVal = ""

    if exists:
        with open('createAAD.json') as f:
            createAADVal = json.load(f)
    else:
        command = 'az ad app create --display-name '+ config_data["display_name"] +' --password '+ client_secret +' --homepage '+ config_data["homepage"] +' --identifier-uris ' + config_data["identifier_uris"]
        output = subprocess.check_output(command.split())
        createAADVal = json.loads(output)

        with open('createAAD.json', 'w') as outfile:
            json.dump(createAADVal, outfile)

    print(createAADVal)

    # client Id
    client_id = createAADVal["appId"]
    print(client_id)
    time.sleep(5)

    # Create and Configure a Service Principal
    exists = os.path.isfile('createAAD.json')
    createCSPVal = ""

    if exists:
        with open('createAAD.json') as f:
            createCSPVal = json.load(f)
    else:
        command = 'az ad sp create --id ' + client_id
        output = subprocess.check_output(command.split())
        createCSPVal = json.loads(output)

        with open('createCSP.json', 'w') as outfile:
            json.dump(createCSPVal, outfile)

    print(createCSPVal)

    time.sleep(5)

    #  assign role to AAD appId
    exists = os.path.isfile('roleAssignment.json')
    roleAssignmentVal = ""

    if exists:
        with open('roleAssignment.json') as f:
            roleAssignmentVal = json.load(f)
    else:
        command = 'az role assignment create --assignee '+client_id+' --role '+ config_data["role_assignment"] +' --scope /subscriptions/' + subscription_id
        output = subprocess.check_output(command.split())
        roleAssignmentVal = json.loads(output)

        with open('roleAssignment.json', 'w') as outfile:
            json.dump(roleAssignmentVal, outfile)

    print(roleAssignmentVal)

    # Verify the assignment
    command = 'az role assignment list --assignee '+ client_id
    output = subprocess.check_output(command.split())
    roleAssignmentList = json.loads(output)

    with open('roleAssignmentList.json', 'w') as outfile:
        json.dump(roleAssignmentList, outfile)
    print(roleAssignmentList)

    if roleAssignmentList[0]["roleDefinitionName"] != config_data["role_assignment"]:
        exit()

    file = open("terraform.tfvars","w")

    # for tfvars_obj in config_data["tfvars"]:
    #     print (tfvars_obj)
    #     for value in tfvars_obj:
    #         print (value)
    #
    #         file.write(“Hello World”)


    file.write('subscription_id       = "'+subscription_id+'"')
    file.write('tenant_id       = "'+tenant_id+'"')
    file.write('client_id       = "'+client_id+'"')
    file.write('client_secret       = "'+client_secret+'"')
    file.write('location       = "'+location+'"')

    file.close()


#calling Terraform script
from python_terraform import *
tf = Terraform(working_dir='.')
tf.plan(no_color=IsFlagged, refresh=False, capture_output=True)
approve = {"skip_plan": True}
print(tf.init(reconfigure=True))
print(tf.plan())
print(tf.apply())
