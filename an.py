#!/usr/bin/env python


import queue

m_1 = b"Client messages are not usually the best, they are broken down into " \
      b"different chunks in order to send them as bytes on the network. This has" \
      b"led to the development of methods that will do break down messages for us" \
      b"minizing our stress level"

m_2 = b'I spent like one week trying to understand how to extract file from binary data' \
      b'Isn\'t that awesome'

m_3 = b'Now that I have that figured out, we can now setup message types and other methods ne' \
      b'cessary to maintain the deterministic finite automata'

m = queue.Queue()
m.put(m_1)
m.put(m_2)
m.put(m_3)

print(m.qsize())

while not m.empty():
    print(m.get())
