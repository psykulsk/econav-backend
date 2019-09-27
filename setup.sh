#!/bin/bash
# Script for simplified setup

# service names
. ./servicenames.sh


# Create AppID service using "bx resource" command. AppID is available with
# resource groups.
ibmcloud resource service-instance-create $AppID_service appid lite eu-de
ibmcloud resource service-alias-create $AppID_service --instance-name $AppID_service -s prod
