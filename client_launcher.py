import subprocess
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(base_dir, "assets", "downloaded.txt")
file = open(filepath,"r")
_,b = file.readline().strip().split("=", 1)
file.close

if b == "False":
    subprocess.Popen(["start", "cmd", "/k", "pip install pynacl keyboard pygame"], shell=True)
    file = open(filepath,"w")
    file.write("downloaded=True")
else:
    subprocess.Popen(["start", "cmd", "/k", "python server.py"], shell=True)
    for i in range(2): # change range for number of clients you want to test with
        subprocess.Popen(["start", "cmd", "/k", "python main.py"] , shell=True)

file.close()