# rip_simple.py

def run_rip_simulation():
    network = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'D'],
        'C': ['A', 'D'],
        'D': ['A', 'B', 'C', 'E'],
        'E': ['D']
    }
    
    routers = list(network.keys())
    tables = {}

    for u in routers:
        tables[u] = {}
        tables[u][u] = (0, u)

    for u in routers:
        for v in network[u]:
            tables[u][v] = (1, v)

    changed = True
    iteration = 0

    print("Simulating RIP...\n")

    while changed:
        changed = False
        iteration += 1
        
        for u in routers:
            for v in network[u]:
                if v not in tables: 
                    continue
                
                neighbor_table = tables[v]
                for dest, (cost, _) in neighbor_table.items():
                    
                    new_cost = 1 + cost
                    
                    if dest not in tables[u] or new_cost < tables[u][dest][0]:
                        tables[u][dest] = (new_cost, v)
                        changed = True

    print(f"*** CONVERGENCE REACHED AFTER {iteration} ITERATIONS ***\n")

    for router in sorted(routers):
        print(f"--- Routing Table for Router {router} ---")
        print(f"| {'Destination':<12} | {'Cost (Hops)':<12} | {'Next Hop':<10} |")
        print(f"|{'-'*14}|{'-'*14}|{'-'*12}|")
        
        for dest in sorted(tables[router].keys()):
            cost, next_hop = tables[router][dest]
            print(f"| {dest:<12} | {cost:<12} | {next_hop:<10} |")
        print("-" * 42 + "\n")

if __name__ == "__main__":
    run_rip_simulation()
