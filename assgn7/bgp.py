# bgp_simulation.py
import time

def run_bgp_simulation():
    
    as_topology = {
        'AS1': ['AS2', 'AS3'],
        'AS2': ['AS1', 'AS4'],
        'AS3': ['AS1', 'AS4'],
        'AS4': ['AS2', 'AS3', 'AS5'],
        'AS5': ['AS4']
    }
    
    as_prefixes = {
        'AS1': '10.1.0.0/16',
        'AS2': '20.2.0.0/16',
        'AS3': '30.3.0.0/16',
        'AS4': '40.4.0.0/16',
        'AS5': '50.5.0.0/16'
    }
    
    all_ases = sorted(as_topology.keys())
    
    routing_tables = {}
    
    for asn in all_ases:
        routing_tables[asn] = {}
        my_prefix = as_prefixes[asn]
        routing_tables[asn][my_prefix] = {
            'path': [asn],
            'next_hop': '-'
        }
        
    print("Simulating BGP convergence...\n")

    changed = True
    iteration = 0
    
    while changed:
        changed = False
        iteration += 1
        
        for u_as in all_ases:
            
            for v_as in as_topology[u_as]:
                
                table_to_advertise = routing_tables[u_as]
                
                for prefix, info in table_to_advertise.items():
                    advertised_path = info['path']
                    
                    if v_as in advertised_path:
                        continue
                        
                    new_path = [v_as] + advertised_path
                    
                    if prefix not in routing_tables[v_as]:
                        routing_tables[v_as][prefix] = {
                            'path': new_path,
                            'next_hop': u_as
                        }
                        changed = True
                    else:
                        current_path = routing_tables[v_as][prefix]['path']
                        if len(new_path) < len(current_path):
                            routing_tables[v_as][prefix] = {
                                'path': new_path,
                                'next_hop': u_as
                            }
                            changed = True

    print(f"*** CONVERGENCE REACHED AFTER {iteration} ITERATIONS ***\n")
    
    for asn in all_ases:
        print(f"--- BGP Table for {asn} ---")
        print(f"| {'Prefix':<15} | {'AS Path Length':<14} | {'Next Hop':<10} | {'AS Path':<20} |")
        print(f"|{'-'*17}|{'-'*16}|{'-'*12}|{'-'*22}|")
        
        for prefix in sorted(routing_tables[asn].keys()):
            info = routing_tables[asn][prefix]
            path_str = " ".join(info['path'])
            print(f"| {prefix:<15} | {len(info['path']):<14} | {info['next_hop']:<10} | {path_str:<20} |")
        print("-" * 71 + "\n")

if __name__ == "__main__":
    run_bgp_simulation()
