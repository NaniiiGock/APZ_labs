import hazelcast
import threading
from argparse import ArgumentParser

def run_client(lock_t):
    client = hazelcast.HazelcastClient(cluster_name="dev")
    dist_map = client.get_map("distributed-map").blocking()
    
    if lock_t == "none":
        for i in range(10000):
            value = dist_map.get("key")
            dist_map.put("key", value+1)

    elif lock_t == "pessimistic":
        for i in range(10000):
            dist_map.lock("key")
            try:
                value = dist_map.get("key")
                dist_map.put("key", value + 1)
            finally:
                dist_map.unlock("key")

    elif lock_t == "optimistic":
        for i in range(10000):
            while True:
                value = dist_map.get("key")
                upd_vaue = value + 1
                if dist_map.replace_if_same("key", value, upd_vaue):
                    break

    client.shutdown()

if __name__ == "__main__":
    parser = ArgumentParser(prog='distributed_map_locks.py')

    parser.add_argument("--lock", "-l", type=str, required=False,
                        default="none", help="Lock type to use (none, pessimistic, optimistic)")

    args = parser.parse_args()
    lock_type = args.lock
    print(f"Lock Type: {lock_type}")
    
    client = hazelcast.HazelcastClient()
    dist_map = client.get_map("distributed-map")
    
    dist_map.lock("key")
    dist_map.put("key", 0)
    dist_map.unlock("key")
    
    threads = []
    for i in range(3):
        thread = threading.Thread(target=run_client, args=(lock_type,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("distributed map got", dist_map.get("key").result())
    client.shutdown()
