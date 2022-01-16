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
            "modify_time": self.modify_time,
            "iso8601_to_servicenow_datetime_format": self.convert_to_sn_datetime_format,
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
            raise AnsibleFilterError(f"modify_time - {to_native(exc)}", orig_exc=exc)
        else:
            return dt.strftime(r"%Y-%m-%d %H:%M:%S")

    def modify_time(
        self,
        dt: str,
        modifier: Optional[str] = "add",
        days: Optional[int] = 0,
        hours: Optional[int] = 0,
        minutes: Optional[int] = 0,
        seconds: Optional[int] = 0,
    ) -> str:
        """Adds or substracts a user-specificed amount of time to/from a datetime string."""
        try:
            dt = datetime.strptime(dt, r"%Y-%m-%dT%H:%M:%SZ")
        except Exception as exc:
            raise AnsibleFilterError(f"modify_time - {to_native(exc)}", orig_exc=exc)
        try:
            td = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        except Exception as exc:
            raise AnsibleFilterError(f"modify_time - {to_native(exc)}", orig_exc=exc)
        if modifier.strip().lower() == "add":
            result = dt + td
        elif modifier.strip().lower() == "subtract":
            result = dt - td
        else:
            raise AnsibleFilterError("modify_time - Invalid time modifier provided")
        return result.strftime(r"%Y-%m-%d %H:%M:%S")
