import subprocess

subprocess.run(["docker", "cp","test1.py","intelligent_goldberg:/testingTF/test1.py"])
subprocess.run(["docker", "cp","test2.py","intelligent_goldberg:/testingTF/test2.py"])
subprocess.run(["docker", "cp","dfCSV.txt","intelligent_goldberg:/testingTF/dfCSV.txt"])
subprocess.run(["docker", "cp","dataset.txt","intelligent_goldberg:/testingTF/dataset.txt"])
subprocess.run(["docker", "exec","-it","intelligent_goldberg", "python3","testingTF/test1.py"])
#subprocess.run(["docker", "exec","-it","intelligent_goldberg", "python3","testingTF/test2.py"])
subprocess.run(["docker", "cp","intelligent_goldberg:/testingTF/plotm1.png","."])
subprocess.run(["docker", "cp","intelligent_goldberg:/testingTF/model_plot.png","."])
