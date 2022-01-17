#!/bin/bash
cd /home/christopher/GitHub/Pluralsight/pluralsight-ansible-itsm
source .venv/bin/activate
ansible-playbook playbooks/module-3/c2_servicenow_fetch_scheduled_change_requests_pauseless.yaml | tee /var/log/m3c2_ansible_playbook.log
