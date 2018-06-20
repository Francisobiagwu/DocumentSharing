#!/usr/bin/env python

__author__ = "Francis Obiagwu"
__copyright__ = "Copyright 2018"
__version__ = "1.0"

from queue import Queue
from queue import LifoQueue

arr = []
with open('testfile', 'r') as file:
    for item, number in enumerate(file):
        arr.append((item, number))



arr_changes = []



print(arr)

q = Queue()
print(q)

def what_changed(old_data, new_data):
    new_arr = [old_data, new_data]
    arr_changes.append(new_arr)
    q.put(new_arr)



def undo():
    #find the last to enter the queue
    #update the arr by swapping the new_data with the old_data
    # the updated array

    last_changes = q.get()
    print(last_changes)
    index = arr.index(last_changes[1])
    change(index, last_changes[0][1])
    print(arr)
    pass


def change(section_no, content):
    for number, section in enumerate(arr):
        if section_no in section:
            edited_section = (section_no, content)
            print(arr)
            print(section)
            what_changed(section, edited_section)
            arr[number] = edited_section

            print(arr)

            return True
        else:
            return False


change(0, 'here')
change(1, 'We are changing the second line to reflect the new changes')
undo()






