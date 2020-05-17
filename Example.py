import requests
import rx
import json
import os
from rx import operators as ops
def filternames(x):
   if (x["name"].startswith("C")):
      return x["name"]
   else :
      return ""
content = requests.get('https://jsonplaceholder.typicode.com/users')
y = json.loads(content.text)
source = rx.from_(y)
case1 = source.pipe(
   ops.filter(lambda c: filternames(c)),
   ops.map(lambda a:a["name"])
)
case1.subscribe(
   on_next = lambda i: print("Got - {0}".format(i)),
   on_error = lambda e: print("Error : {0}".format(e)),
   on_completed = lambda: print("Job Done!"),
)


myinput_path = "/dev/shm/myinput.txt"


def getmodifieddate(file_path):
   return os.path.getmtime(file_path)

print(getmodifieddate(myinput_path))

rx.interval(1).subscribe_(print)


input("press any key to exit")