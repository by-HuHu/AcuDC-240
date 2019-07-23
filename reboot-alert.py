#!/usr/bin/env python
#Python 2.7
#Script to report a reboot from the raspberry pi
#It sends a message to ********@********

import subprocess

subprocess.call('echo "Raspberry pi was rebooted. You might want to check it." | mail -s "Rasperry pi reboot" *****@*****', shell = True)
