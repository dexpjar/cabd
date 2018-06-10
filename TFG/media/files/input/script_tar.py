import sys
import os

name_zip = sys.argv[1]

dir_remote_output = "/home/ftpsUser/output/" + task_select.taskcode + "/"

os.system('tar -zcvf '+name_zip+' '+dir_remote_output)
