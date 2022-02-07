from subprocess import Popen
import sys

while True:
    print("\nStarting link forwarder")
    p = Popen("python3 main.py", shell=True)
    p.wait()
