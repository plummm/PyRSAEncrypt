import os

def create_dir(path):
  if not os.path.exists(path):
	os.mkdir(path)

def hello(path):
  with open(path+"/Hello.txt", "w") as f:
	f.write("Hello World\n")
	f.close()

