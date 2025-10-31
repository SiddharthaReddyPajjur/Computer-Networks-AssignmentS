def ip_to_binary(ip_address: str) -> str:
    octets = ip_address.split('.')
    binary_octets = [f'{int(octet):08b}' for octet in octets]
    return "".join(binary_octets)

def get_network_prefix(ip_cidr: str) -> str:
    ip_address, prefix_length_str = ip_cidr.split('/')
    prefix_length = int(prefix_length_str)
    full_binary_ip = ip_to_binary(ip_address)
    return full_binary_ip[:prefix_length]

if __name__ == "__main__":
    print("--- Testing Part 1: ip_utils.py ---")
    
    test_ip = "192.168.1.1"
    expected_binary = "11000000101010000000000100000001"
    result_binary = ip_to_binary(test_ip)
    print(f"ip_to_binary('{test_ip}')")
    print(f"  Result:   {result_binary}")
    print(f"  Expected: {expected_binary}")

    test_ip_2 = "200.23.16.0"
    expected_binary_2 = "11001000000101110001000000000000"
    result_binary_2 = ip_to_binary(test_ip_2)
    print(f"\nip_to_binary('{test_ip_2}')")
    print(f"  Result:   {result_binary_2}")
    print(f"  Expected: {expected_binary_2}")

    test_cidr = "200.23.16.0/23"
    expected_prefix = "11001000000101110001000"
    result_prefix = get_network_prefix(test_cidr)
    print(f"\nget_network_prefix('{test_cidr}')")
    print(f"  Result:   {result_prefix}")
    print(f"  Expected: {expected_prefix}")

