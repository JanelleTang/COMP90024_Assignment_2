

export ANSIBLE_HOST_KEY_CHECKING=False
. ./openrc.sh; ansible-playbook --ask-become-pass DeployApplication.yaml -i inventory/inventory.ini