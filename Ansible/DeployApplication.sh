# ============= COMP90024 - Assignment 2 ============= #
#                               
# The University of Melbourne           
# Team 37
#
# ** Authors: **
# 
# JJ Burke              1048105
# Janelle Tang          694209
# Shuang Qiu            980433
# Declan Baird-Watson   640975
# Avinash Rao           1024577 
# 
# Location: Melbourne
# ==================================================== 

export ANSIBLE_HOST_KEY_CHECKING=False
. ./openrc.sh; ansible-playbook --ask-become-pass DeployApplication.yaml -i inventory/inventory.ini --private-key ~/.ssh/dev-testing.pem
