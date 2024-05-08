import hazelcast
import threading


def write_to_queue():
    client = hazelcast.HazelcastClient(cluster_name="dev")
    queue = client.get_queue("bounded-queue").blocking()
    print("Writing...")
    for i in range(1, 101):
        queue.put(i)
        print("Wrote:", i)
    print("Writing finished")
    client.shutdown()

def read_from_queue(num=None):
    client = hazelcast.HazelcastClient(cluster_name="dev")
    if num is None:
        queue = client.get_queue("bounded-queue")
        while True:
            future = queue.poll()
            if future is not None:
                value = future.result() 
                print("Reading:", value)
            else:
                print("Empty Queue")
                break
    else:
        queue = client.get_queue("bounded-queue").blocking()
        num_empty = 0
        while True:
            future = queue.poll()
            if future is not None:
                print(f"Reading on {num}: {future}")
                num_empty = 0
            else:
                num_empty += 1
            if num_empty > 10:
                print("Empty Queue on ", num)
                break
            
    client.shutdown()


if __name__ == "__main__":
    thread_writing = threading.Thread(target=write_to_queue)
    thread_writing.start()

    # thread1_reading = threading.Thread(target=read_from_queue, args=(1,))
    # thread1_reading.start()
    
    # thread2_reading = threading.Thread(target=read_from_queue, args=(2,))
    # thread2_reading.start()

    thread_writing.join()
    # thread1_reading.join()
    # thread2_reading.join()
