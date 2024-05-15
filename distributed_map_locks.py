import hazelcast
import threading
from argparse import ArgumentParser

def run_blocking(lock_t):
    client = hazelcast.HazelcastClient(cluster_name="dev")
    dist_map = client.get_map("distributed-map").blocking()
    if lock_t == "none":
        for i in range(10000):
            dist_map.put("key", dist_map.get("key")+1)
            
    elif lock_t == "optimistic":
        for i in range(10000):
            while True:
                if dist_map.replace_if_same("key", \
                                dist_map.get("key"), \
                                dist_map.get("key")+1):
                    break
    else:
        for i in range(10000):
            dist_map.lock("key")
            try:
                dist_map.put("key", dist_map.get("key")+1)
            finally:
                dist_map.unlock("key")
    client.shutdown()

if __name__ == "__main__":
    parser = ArgumentParser(prog='distributed_map_locks.py')
    parser.add_argument("--lock", type=str)
    args = parser.parse_args()
    print(f"Lock Type: {args.lock}")
    
    dist_map = hazelcast.HazelcastClient().get_map("distributed-map")
    dist_map.lock("key")
    dist_map.put("key", 0)
    dist_map.unlock("key")

    threads = []
    for i in range(3):
        thread = threading.Thread(target=run_blocking, args=(args.lock,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("distributed map got", dist_map.get("key").result())
