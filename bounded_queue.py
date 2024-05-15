import hazelcast
import threading


def read_from_queue(num=None):
    client = hazelcast.HazelcastClient(cluster_name="dev")
    
    flag = False
    if num is not None:
        flag = True
        
    if flag:
        queue = client.get_queue("bounded-queue").blocking()
        num_empty = 0
    else:
        queue = client.get_queue("bounded-queue")
    
    num_empty = 0
    while True:
        future = queue.poll()
        if future is not None:
            print(f"Reading on {num}: {future}") if flag else print("Reading:", future.result())
            num_empty = 0
        else:
            print("Empty Queue on ", num) if flag else print("Empty Queue")
            num_empty += 1
            break
    client.shutdown()

def write_to_queue():
    client = hazelcast.HazelcastClient(cluster_name="dev")
    queue = client.get_queue("bounded-queue").blocking()
    print("Writing...")
    for i in range(1, 101):
        queue.put(i)
        print("put:", i)
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
