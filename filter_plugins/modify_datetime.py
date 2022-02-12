#!/usr/bin/python
"""Contains Ansible filter plugins used to modify datetime strings."""

from typing import Optional, Dict
from datetime import datetime, timedelta
from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_native


class FilterModule:
    """Contains Ansible filter plugins used to modify datetime strings."""

    def filters(self) -> Dict:
        """Maps filter plugin names to functions.

        This function is required by Ansible for custom filter plugins to work. The key of each
        key-value pair in the returned dictionary is the name of the filter called by Ansible. The
        value of each key-value pair is the function within the FilterModule class that will be
        called by Ansible when the filter is called.
        """
        return {
            "modify_time_sn": self.modify_time_sn,
            "modify_time_jira": self.modify_time_jira,
            "iso8601_to_servicenow_datetime_format": self.convert_to_sn_datetime_format,
            "iso8601_to_jira_datetime_format": self.convert_to_jira_datetime_format,
        }

    def convert_to_sn_datetime_format(self, dt: str) -> str:
        """Convert Ansible datetime strings to ServiceNow datetime strings.

        This filter will convert a datetime string commonly used by Ansible (which is in a
        "%Y-%m-%DT%H:%M:%SZ" format, such as "2022-01-16T16:39:43Z") into a datetime string
        commonly used by ServiceNow (which is in a "%Y-%m-%D %H:%M:%S" format, such as
        "2022-01-16 16:39:43").
        """
        try:
            dt = datetime.strptime(dt, r"%Y-%m-%dT%H:%M:%SZ")
        except Exception as exc:
            raise AnsibleFilterError(
                f"convert_to_sn_datetime_format - {to_native(exc)}", orig_exc=exc
            )
        else:
            return dt.strftime(r"%Y-%m-%d %H:%M:%S")

    def convert_to_jira_datetime_format(
        self,
        dt: str,
        add_offset_hours: int = None,
        subtract_offset_hours: int = None,
    ) -> str:
        """Convert Ansible datetime strings to Jira datetime strings.

        This filter will convert a datetime string commonly used by Ansible (which is in a
        "%Y-%m-%DT%H:%M:%SZ" format, such as "2022-01-16T16:39:43Z") into a datetime string
        commonly used by Jira (which is in a "%Y-%m-%dT%H:%M:%SZ" format, such as
        "2022-02-06T09:50:37Z")
        """
        try:
            dt = datetime.strptime(dt, r"%Y-%m-%dT%H:%M:%SZ")
        except Exception as exc:
            raise AnsibleFilterError(
                f"convert_to_jira_datetime_format - {to_native(exc)}", orig_exc=exc
            )
        else:
            if add_offset_hours:
                dt = dt + timedelta(hours=add_offset_hours)
            if subtract_offset_hours:
                dt = dt - timedelta(hours=subtract_offset_hours)
            return dt.strftime(r"%Y-%m-%d %H:%M")

    def modify_time(
        self,
        dt: datetime,
        modifier: Optional[str] = "add",
        days: Optional[int] = 0,
        hours: Optional[int] = 0,
        minutes: Optional[int] = 0,
        seconds: Optional[int] = 0,
    ) -> datetime:
        """Adds or substracts a user-specificed amount of time to/from a datetime string."""
        try:
            td = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        except Exception as exc:
            raise AnsibleFilterError(f"modify_time - {to_native(exc)}", orig_exc=exc)
        if modifier.strip().lower() == "add":
            return dt + td
        elif modifier.strip().lower() == "subtract":
            return dt - td
        else:
            raise AnsibleFilterError("modify_time - Invalid time modifier provided")

    def modify_time_sn(
        self,
        ansible_dt: str,
        modifier: Optional[str] = "add",
        days: Optional[int] = 0,
        hours: Optional[int] = 0,
        minutes: Optional[int] = 0,
        seconds: Optional[int] = 0,
    ) -> str:
        """Add/subtract amount of time to/from datetime string and return in ServiceNow format."""
        try:
            dt = datetime.strptime(ansible_dt, r"%Y-%m-%dT%H:%M:%SZ")
        except Exception as exc:
            raise AnsibleFilterError(f"modify_time_sn - {to_native(exc)}", orig_exc=exc)
        result_dt = self.modify_time(
            dt,
            modifier=modifier,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )
        return result_dt.strftime(r"%Y-%m-%d %H:%M:%S")

    def modify_time_jira(
        self,
        ansible_dt: str,
        modifier: Optional[str] = "add",
        days: Optional[int] = 0,
        hours: Optional[int] = 0,
        minutes: Optional[int] = 0,
        seconds: Optional[int] = 0,
        planned_date: bool = True,
    ) -> str:
        """Add/subtract amount of time to/from datetime string and return in Jira format."""
        try:
            dt = datetime.strptime(ansible_dt, r"%Y-%m-%dT%H:%M:%SZ")
        except Exception as exc:
            raise AnsibleFilterError(
                f"modify_time_jira - {to_native(exc)}", orig_exc=exc
            )
        result_dt = self.modify_time(
            dt,
            modifier=modifier,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        )
        if planned_date:
            return result_dt.strftime(r"%Y-%m-%dT%H:%M:%SZ")
        return result_dt.strftime(r"%Y-%m-%d %H:%M")
