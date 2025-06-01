import time
from node import Cluster


if __name__ == "__main__":
    num = int(input("Enter number of nodes: "))
    cluster = Cluster(num)

    node_id = int(input("Set the node to be the leader: "))
    cluster.set_leader(id=node_id)

    cluster.start()

    try:
        while True:
            print("\nMenu:")
            print("1. Show node status")
            print("2. Send PING to leader")
            print("3. Send ELECTION message from node")
            print("4. Exit")
            choice = input("Enter choice: ")

            if choice == "1":
                for i in range(num):
                    cluster.print_status(i)
            elif choice == "2":
                from_id = int(input("Enter sender node id: "))
                leader_id = cluster.get_leader_id()
                if leader_id is None:
                    print("No leader currently.")
                else:
                    cluster.send_message(from_id, leader_id, "PING")
            elif choice == "3":
                from_id = int(input("Enter node id starting election: "))
                cluster.send_message(from_id, from_id, "ELECTION")
            elif choice == "4":
                break
            else:
                print("Invalid choice.")
    finally:
        cluster.stop()
        print("Cluster shut down.")
