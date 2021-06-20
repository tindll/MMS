import subprocess

subprocess.run(["docker", "cp","test1.py","intelligent_goldberg:/testingTF/test1.py"])
subprocess.run(["docker", "exec","-it","intelligent_goldberg", "python3","testingTF/test1.py"])