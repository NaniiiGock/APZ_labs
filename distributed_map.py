import hazelcast
client = hazelcast.HazelcastClient(
  cluster_name="dev", 
  ) 

distributed_map = client.get_map("my-distributed-map").blocking()

for i in range(1000):
    distributed_map.put("key-" + str(i), "value-" + str(i))
