"""This module contains a simple FastAPI webhook receiver that executes Ansible automation."""

from typing import Optional
import os
import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks
import ansible_runner

app = FastAPI()
worked_issues = []


@app.post("/servicenow/{servicenow_record}", status_code=200)
async def servicenow_connectivity_issue_webhook(
    servicenow_record: str,
    request: Request,
    background_tasks: BackgroundTasks,
) -> None:
    """Execute Ansible automation that troubleshoots a connectivity issue defined in ServiceNow."""
    global worked_issues
    body = await request.json()
    # Uncomment the below if you would like to see the full body of the webhook
    # from pprint import pprint
    # pprint(body)

    if servicenow_record in worked_issues:
        print(
            f"Ignoring received webhook for ServiceNow record {servicenow_record} because we have "
            "already worked it"
        )
        return

    record_creator = body["reported_by_email"]
    source_ip = body["source_ip"]
    destination_ip = body["destination_ip"]
    print(
        f"Received webhook for ServiceNow record {servicenow_record} created by {record_creator}. "
        f"Need to troubleshoot connectivity between {source_ip} and {destination_ip}."
    )
    worked_issues.append(servicenow_record)

    # Uncomment the below if you would like to run the basic connectivity issue troubleshooting
    # Ansible playbook.
    # background_tasks.add_task(
    #     execute_ansible_playbook,
    #     "playbooks/module-4/c4_servicenow_basic_connectivity_issue_troubleshooting.yaml",
    #     source_ip,
    #     destination_ip,
    #     extra_variables={"servicenow_record": servicenow_record},
    # )

    # Uncomment the below if you would like to run the advanced connectivity issue troubleshooting
    # Ansible playbook.
    # background_tasks.add_task(
    #     execute_ansible_playbook,
    #     "playbooks/module-4/c5_servicenow_advanced_connectivity_issue_troubleshooting.yaml",
    #     source_ip,
    #     destination_ip,
    #     extra_variables={"servicenow_record": servicenow_record},
    # )

    # Uncomment the below if you would like to run the advanced connectivity issue troubleshooting
    # and automatic incident resolution Ansible playbook.
    background_tasks.add_task(
        execute_ansible_playbook,
        "playbooks/module-4/c6_servicenow_connectivity_issue_resolution.yaml",
        source_ip,
        destination_ip,
        extra_variables={"servicenow_record": servicenow_record},
    )


@app.post("/jira/{jira_issue_key}", status_code=200)
async def jira_connectivity_issue_webhook(
    jira_issue_key: str, request: Request, background_tasks: BackgroundTasks
) -> None:
    """Execute Ansible automation that troubleshoots a connectivity issue defined in Jira."""
    global worked_issues
    body = await request.json()
    # Uncomment the below if you would like to see the full body of the webhook
    # from pprint import pprint
    # pprint(body)

    if jira_issue_key in worked_issues:
        print(
            f"Ignoring received webhook for Jira issue {jira_issue_key} because we have already "
            "worked it"
        )
        return

    issue_creator = body["user"]["displayName"]
    source_ip = body["issue"]["fields"]["customfield_10060"]
    destination_ip = body["issue"]["fields"]["customfield_10061"]
    print(
        f"Received webhook for Jira issue {jira_issue_key} created by "
        f"{issue_creator}. Need to troubleshoot connectivity between "
        f"{source_ip} and {destination_ip}."
    )
    worked_issues.append(jira_issue_key)

    # Uncomment the below if you would like to run the basic connectivity issue troubleshooting
    # Ansible playbook.
    # background_tasks.add_task(
    #     execute_ansible_playbook,
    #     "playbooks/module-7/c4_jira_basic_connectivity_issue_troubleshooting.yaml",
    #     source_ip,
    #     destination_ip,
    #     extra_variables={"jira_issue_key": jira_issue_key},
    # )

    # Uncomment the below if you would like to run the advanced connectivity issue troubleshooting
    # Ansible playbook.
    # background_tasks.add_task(
    #     execute_ansible_playbook,
    #     "playbooks/module-7/c5_jira_advanced_connectivity_issue_troubleshooting.yaml",
    #     source_ip,
    #     destination_ip,
    #     extra_variables={"jira_issue_key": jira_issue_key},
    # )

    # Uncomment the below if you would like to run the advanced connectivity issue troubleshooting
    # and automatic incident resolution Ansible playbook.
    background_tasks.add_task(
        execute_ansible_playbook,
        "playbooks/module-7/c6_jira_connectivity_issue_resolution.yaml",
        source_ip,
        destination_ip,
        extra_variables={"jira_issue_key": jira_issue_key},
    )


def execute_ansible_playbook(
    playbook_filepath: str,
    source_ip: str,
    destination_ip: str,
    extra_variables: Optional[dict] = None,
) -> None:
    """Executes a user-defined Ansible playbook, passing in source and destination IP addresses."""
    cwd = os.getcwd()
    extravars = {
        "source_ip": source_ip,
        "destination_ip": destination_ip,
    }
    if extra_variables:
        extravars = {**extravars, **extra_variables}
    runner_config = ansible_runner.runner_config.RunnerConfig(
        **{
            "private_data_dir": cwd,
            "playbook": f"{cwd}/{playbook_filepath}",
            "inventory": f"{cwd}/inventory.yaml",
            "envvars": {"ANSIBLE_CONFIG": f"{cwd}/ansible.cfg"},
            "extravars": extravars,
        }
    )
    runner_config.prepare()

    runner = ansible_runner.Runner(config=runner_config)
    runner.run()


if __name__ == "__main__":
    uvicorn.run("fastapi_webhook_handler:app", host="0.0.0.0", port=8443, reload=True)
