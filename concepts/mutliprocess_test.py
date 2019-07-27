import multiprocessing
import queue

class BigThing:
    def __init__(self, number):
        self.number = number
        attributes = []
        for a in range(10000):
            for b in range(1000):
                attributes.append("Hello")

    def __str__(self):
        return str(self.number)


def createBigThings(things_to_make, things_made):
    while True:
        try:
            number = things_to_make.get_nowait()
        except queue.Empty:
            break
        else:
            things_made.put(BigThing(number))
            print("Finished thing %d" % number)


def main():
    number_of_big_things = 100
    number_of_processes = 4
    things_to_make = multiprocessing.Queue()
    things_made = multiprocessing.Queue()

    processes = []

    for i in range(number_of_big_things):
        things_to_make.put(i)

    # Create processes
    for p in range(number_of_processes):
        p = multiprocessing.Process(target=createBigThings, args=(things_to_make, things_made))
        processes.append(p)


    for d in processes:
        d.start()
        d.join()
        print("Killed")

if __name__ == '__main__':
    main()