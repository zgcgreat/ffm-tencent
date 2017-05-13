# -*- encoding:utf-8 -*-
import subprocess

cmd = 'python csv_2_ffm.py'
subprocess.call(cmd, shell=True)

cmd = 'python ffm.py'
subprocess.call(cmd, shell=True)


