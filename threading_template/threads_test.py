from time import sleep
import threading
from queue import Queue

def printstuff(stuff):
    while True:
        sleep(1)
        print(stuff)

if __name__ == "__main__":


    #create threads
    threads = [threading.Thread(target=printstuff, args=(i, )) for i in range(4)]

    #start threads
    for t in threads:
        t.start()
