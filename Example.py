import rx
import os
from rx import operators as ops

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


# Every second
file_check_interval_observable = rx.interval(1)

# Print elapsed second
file_check_interval_observable.subscribe(print)

#emit modified date every second, if the date has changed since last time.
file_changed_observable = file_check_interval_observable.pipe(
   ops.map(lambda i: get_modified_date(myinput_path)),
   ops.distinct_until_changed()
)

#Debug subscription to show when modified date gets printed out.
file_changed_observable.subscribe(
   on_next = lambda i: print("Got date modified - {0}".format(i)),
   on_error = lambda e: print("Error : {0}".format(e)),
   on_completed = lambda: print("Job Done!"),
)

#When a emission is produced upstream, read contents of the new file.
file_changed_observable.subscribe(lambda ignore: read_file_contents(myinput_path))

#Hang main execution so that rx async runs.
input("press any key to exit")
