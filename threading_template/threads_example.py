from time import sleep
import threading
from queue import Queue

def printstuff(stuff):
    while True:
        print(stuff.get())

if __name__ == "__main__":

    #pipeline to talk to threads
    stuff = Queue()

    #create threads
    t1 = threading.Thread(target=printstuff, args=(stuff,))
    t2 = threading.Thread(target=printstuff, args=(stuff,))

    #start threads
    t1.start()
    t2.start()

    stuff.put("Howdy")
    stuff.put("World")
