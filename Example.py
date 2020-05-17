import time

import rx
import os
from rx import operators as ops
from rx.subject import BehaviorSubject

"""
This code will check modified date of a file every second and, 
if the modified date has changed since last read
reread the file contents.
"""


myinput_path = "/dev/shm/myinput.txt"


def get_modified_date(file_path):
   return os.path.getmtime(file_path)

def read_file_contents(file_path):
   with open(file_path, 'r') as reader:
      # Read and print the entire file line by line
      for line in reader:
         print(line, end='')


def intense_calculation(value, i):
   # sleep for 10 seconds to simulate a long-running calculation so we can see how the code handles it.
   print("Sleeping for 10 seconds "+str(i))
   time.sleep(10)
   return value


# Every second
file_check_interval_observable = rx.interval(1)

# Print elapsed second
file_check_interval_observable.subscribe(print)

#emit modified date every second, if the date has changed since last time.
#use a connectable observable so that multiple downstreams
#all use the same file polling.
file_changed_observable = file_check_interval_observable.pipe(
   #Uncomment this to see what happens if file takes 10 seconds to load.
   #ops.map(lambda i: intense_calculation(myinput_path, i)),
   ops.map(lambda i: get_modified_date(myinput_path)),
   ops.distinct_until_changed(),
   #Without this each subscriber would create a new stream
   #So we'd have one modification date check for the debug statement below
   #and one for the debug, which is unnecessary.

   #Replay ensures late subscribers
   #will read the file.
   ops.replay(buffer_size=1),
   ops.ref_count()
)

#Debug subscription to show when modified date gets printed out.
file_changed_observable.subscribe(
   on_next = lambda i: print("Got date modified - {0}".format(i)),
   on_error = lambda e: print("Error : {0}".format(e)),
   on_completed = lambda: print("Job Done!"),
)

#sleep 15 seconds, to test if a late subscriber will get an emission before a file change
#(it should).
#time.sleep(15)

#When a emission is produced upstream, read contents of the new file.
file_changed_observable.subscribe(lambda ignore: read_file_contents(myinput_path))


#Hang main execution so that rx async runs.
input("press any key to exit")
