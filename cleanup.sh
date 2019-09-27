#!/bin/bash
# Cleanup resources


# service names
. ./servicenames.sh

# Delete AppID
ibmcloud resource service-instance-delete $AppID_service
