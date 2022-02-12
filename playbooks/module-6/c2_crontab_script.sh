#!/bin/bash
cd /home/christopher/GitHub/Pluralsight/pluralsight-ansible-itsm
source .venv/bin/activate
ansible-playbook playbooks/module-6/c2_jira_fetch_scheduled_change_requests_pauseless.yaml | tee /var/log/m6c2_ansible_playbook.log
