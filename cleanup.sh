#!/bin/bash
# Cleanup resources


# service names
. ./servicenames.sh

# Delete AppID
ibmcloud resource service-binding-delete $AppID_service $AppID_service
ibmcloud resource service-alias-delete $AppID_service -g hackzurich
ibmcloud resource service-instance-delete $AppID_service
