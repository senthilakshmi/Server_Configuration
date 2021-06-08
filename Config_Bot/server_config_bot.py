""" 
    Codename: server_config_bot.py

    Author: Kumaran Ramalingam 

    Parent Codename:  do_main.py
"""

# Importing Libraries

import json
import logging
import os
from datetime import datetime as dt

# from subprocess import PIPE, Popen, run

from file_copy import Filecopy
from file_edit import FileEdit

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Execute_bot(object):
    @staticmethod
    def execute(user):
        """A Bot to perform server configuration with json input"""

        path = "/dummyfs/%s" % user

        # This segment of code is for filesystem related executions on requested server

        if os.path.lexists(os.path.join(path, "filesystems.json")):
            pass

        # This segment of code is for netgroup related executions on requested server

        if os.path.lexists(
            os.path.join(path, "netgroups.json")
        ):  # checking for file existence

            # For Copying required file for Netgroup change related operations
            logger.info(" ---------- File backup started ----------")
            Filecopy.backup("/etc/passwd")
            Filecopy.backup("/etc/nsswitch.conf")
            Filecopy.backup("/etc/group")
            logger.info(" ---------- File backup Completed ----------")
            # Filecopy.backup("/etc/shadow")

            with open(
                os.path.join(path, "netgroups.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname()[1]:
                    netgroup_name = json_loader[i]["Netgroup"]

                    # Delicate file edit based on actual configuration requirement
                    FileEdit.append_mode("/etc/passwd", netgroup_name)
                    FileEdit.append_mode("/etc/group", "+:::")

                    search_patterns = [
                        "passwd:.+",
                        "group:.+",
                        "shadow:.+",
                        "netgroup:.+",
                    ]
                    replace_patterns = [
                        "passwd:    files sssd",
                        "group:    files nis sssd",
                        "shadow:    compat",
                        "netgroup:    files nis nisplus",
                    ]

                    FileEdit.find_replace(
                        "/tmp/nsswitch.conf", search_patterns, replace_patterns
                    )

                    Filecopy.copy_file("/tmp/nsswitch.conf", "/etc/nsswitch.conf")
                    logger.info(" %s NETGROUP REQUEST COMPLETED" % netgroup_name)

        # This segment of code is for pubkeys related executions on requested server

        if os.path.lexists(
            os.path.join(path, "pubkeys.json")
        ):  # checking for file existence

            with open(
                os.path.join(path, "cronusers.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

        # This segment of code is for pubkeys related executions on requested server

        if os.path.lexists(os.path.join(path, "user_groups.json")):
            pass

        # This segment of code is for softwares related executions on requested server

        if os.path.lexists(os.path.join(path, "softwares.json")):
            pass

        # This segment of code is for cronusers related executions on requested server

        if os.path.lexists(
            os.path.join(path, "cronusers.json")
        ):  # checking for file existence

            # For Copying required file for Netgroup change related operations
            logger.info(" ---------- File backup started ----------")
            Filecopy.backup("/etc/cron.allow")
            logger.info(" ---------- File backup Completed ----------")

            with open(
                os.path.join(path, "cronusers.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname().nodename:
                    cron_user_name = json_loader[i]["User account"]

                    FileEdit.append_mode("/etc/cron.allow", cron_user_name)
                    logger.info(
                        " %s USER HAS BEEN ALLOWED FOR CRONTAB EDIT" % cron_user_name
                    )
