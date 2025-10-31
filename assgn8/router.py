from ip_utils import ip_to_binary, get_network_prefix

class Router:
    
    def __init__(self, routes: list):
        self.forwarding_table = self._build_forwarding_table(routes)

    def _build_forwarding_table(self, routes: list):
        internal_table = []
        for cidr_prefix, output_link in routes:
            binary_prefix = get_network_prefix(cidr_prefix)
            internal_table.append((binary_prefix, output_link))
        
        internal_table.sort(key=lambda item: len(item[0]), reverse=True)
        return internal_table

    def route_packet(self, dest_ip: str) -> str:
        binary_ip = ip_to_binary(dest_ip)
        
        for prefix, output_link in self.forwarding_table:
            if binary_ip.startswith(prefix):
                return output_link
        
        return "Default Gateway"

if __name__ == "__main__":
    print("--- Testing Part 2: router.py ---")
    
    routes_list = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    
    router = Router(routes_list)
    
    ip1 = "223.1.1.100"
    link1 = router.route_packet(ip1)
    print(f"\nroute_packet('{ip1}') -> '{link1}' (Expected: 'Link 0')")

    ip2 = "223.1.2.5"
    link2 = router.route_packet(ip2)
    print(f"route_packet('{ip2}') -> '{link2}' (Expected: 'Link 1')")

    ip3 = "223.1.250.1"
    link3 = router.route_packet(ip3)
    print(f"route_packet('{ip3}') -> '{link3}' (Expected: 'Link 4 (ISP)')")

    ip4 = "198.51.100.1"
    link4 = router.route_packet(ip4)
    print(f"route_packet('{ip4}') -> '{link4}' (Expected: 'Default Gateway')")

