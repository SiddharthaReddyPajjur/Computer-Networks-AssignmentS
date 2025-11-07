# isis_simulation.py
import heapq

def run_isis_simulation():
    
    network_graph = {
        'A': {'B': 5, 'C': 2},
        'B': {'A': 5, 'C': 1, 'D': 3},
        'C': {'A': 2, 'B': 1, 'D': 1},
        'D': {'B': 3, 'C': 1, 'E': 4},
        'E': {'D': 4}
    }
    
    routers = sorted(network_graph.keys())
    
    print("Simulating IS-IS...\n")
    
    for start_node in routers:
        
        distances = {n: float('inf') for n in routers}
        prev_nodes = {n: None for n in routers}
        distances[start_node] = 0
        pq = [(0, start_node)]
        
        while pq:
            current_dist, current_node = heapq.heappop(pq)
            
            if current_dist > distances[current_node]:
                continue
                
            for neighbor, weight in network_graph[current_node].items():
                distance = current_dist + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    prev_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
        
        
        print(f"--- Routing Table for Router {start_node} ---")
        print(f"| {'Destination':<12} | {'Total Cost':<10} | {'Next Hop':<10} |")
        print(f"|{'-'*14}|{'-'*12}|{'-'*12}|")

        for dest in routers:
            if dest == start_node:
                print(f"| {dest:<12} | {0:<10} | {start_node:<10} |")
                continue
            
            if distances[dest] == float('inf'):
                print(f"| {dest:<12} | {'inf':<10} | {'-':<10} |")
                continue

            path_node = dest
            next_hop = None
            while path_node != start_node:
                if prev_nodes[path_node] == start_node:
                    next_hop = path_node
                    break
                path_node = prev_nodes[path_node]
            
            print(f"| {dest:<12} | {distances[dest]:<10} | {next_hop:<10} |")
        print("-" * 40 + "\n")


if __name__ == "__main__":
    run_isis_simulation()
