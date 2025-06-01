from queue import Queue
import threading
import time

class Node:
    def __init__(self, id: int, q: Queue, priority_number: int, cluster_ref):
        self.id = id
        self.queue = q
        self.is_alive = True
        self.is_leader = False
        self.priority_number = priority_number
        self.cluster = cluster_ref  
        self.known_leader = None

    def run(self):
        print(f"Node {self.id} started with priority {self.priority_number}.")
        while self.is_alive:
            try:
                sender_priority, msg = self.queue.get(timeout=1)
                print(f"[Node {self.id}] received '{msg}' from priority {sender_priority}")

                if msg == "PING":
                    if self.is_leader:
                        print(f"[Node {self.id}] is leader. Responding with ALIVE.")
                        sender = self.cluster.get_node_by_priority(sender_priority)
                        self.cluster.send_message(self.id, sender.id, "ALIVE")
                elif msg == "ALIVE":
                    print(f"[Node {self.id}] received ALIVE. Leader is alive.")
                elif msg == "ELECTION":
                    print(f"[Node {self.id}] Election started by lower-priority node.")
                    higher_nodes = self.cluster.get_higher_priority_nodes(self.priority_number)
                    if higher_nodes:
                        for n in higher_nodes:
                            self.cluster.send_message(self.id, n.id, "ELECTION")
                    else:
                        print(f"[Node {self.id}] has highest priority. Becoming leader.")
                        self.is_leader = True
                        self.known_leader = self.id
                        self.cluster.announce_victory(self.id)
                elif msg == "VICTORY":
                    print(f"[Node {self.id}] New leader is node with priority {sender_priority}")
                    self.known_leader = self.cluster.get_node_by_priority(sender_priority).id
                    self.is_leader = False
            except:
                continue
            time.sleep(0.1)


class Cluster:
    def __init__(self, num_nodes: int):
        self.nodes: list[Node] = []
        for i in range(num_nodes):
            q = Queue()
            priority = i + 1
            node = Node(i, q, priority, self)
            self.nodes.append(node)

    def start(self):
        self.threads = []
        for node in self.nodes:
            t = threading.Thread(target=node.run)
            t.start()
            self.threads.append(t)

    def stop(self):
        for node in self.nodes:
            node.is_alive = False
        for t in self.threads:
            t.join()

    def print_status(self, id: int = None):
        if id is not None:
            nodes = [self.nodes[id]]
        else:
            nodes = self.nodes
        for node in nodes:
            status = "Leader" if node.is_leader else "Normal"
            print(f"  Node {node.id} | Priority: {node.priority_number} | {status}")

    def set_leader(self, id: int):
        node = self.nodes[id]
        node.is_leader = True
        node.known_leader = id
        print(f"[Cluster] Node {id} set as leader.")

    def send_message(self, from_id: int, to_id: int, msg: str):
        sender = self.nodes[from_id]
        receiver = self.nodes[to_id]
        receiver.queue.put((sender.priority_number, msg))

    def get_node_by_priority(self, priority: int) -> Node:
        for node in self.nodes:
            if node.priority_number == priority:
                return node
        raise ValueError("No node with such priority.")

    def get_leader_id(self) -> int | None:
        for node in self.nodes:
            if node.is_leader:
                return node.id
        return None

    def get_higher_priority_nodes(self, priority: int) -> list[Node]:
        return [n for n in self.nodes if n.priority_number > priority and n.is_alive]

    def announce_victory(self, leader_id: int):
        for node in self.nodes:
            if node.id != leader_id:
                self.send_message(leader_id, node.id, "VICTORY")
        print(f"[Cluster] Node {leader_id} announced as new leader.")
