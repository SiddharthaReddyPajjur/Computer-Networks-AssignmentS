from dataclasses import dataclass
from typing import List

@dataclass
class Packet:
    source_ip: str
    dest_ip: str
    payload: str
    priority: int

def fifo_scheduler(packet_list: List[Packet]) -> List[Packet]:
    return list(packet_list)

def priority_scheduler(packet_list: List[Packet]) -> List[Packet]:
    return sorted(packet_list, key=lambda packet: packet.priority)

if __name__ == "__main__":
    print("--- Testing Part 3: scheduler.py ---")

    packets_in_arrival_order = [
        Packet(source_ip="10.1.1.2", dest_ip="10.2.2.3", payload="Data Packet 1", priority=2),
        Packet(source_ip="10.1.1.3", dest_ip="10.2.2.4", payload="Data Packet 2", priority=2),
        Packet(source_ip="20.1.1.2", dest_ip="20.2.2.3", payload="VOIP Packet 1", priority=0),
        Packet(source_ip="30.1.1.2", dest_ip="30.2.2.3", payload="Video Packet 1", priority=1),
        Packet(source_ip="20.1.1.5", dest_ip="20.2.2.6", payload="VOIP Packet 2", priority=0)
    ]

    print("\nTesting FIFO Scheduler:")
    fifo_output = fifo_scheduler(packets_in_arrival_order)
    fifo_payloads = [p.payload for p in fifo_output]
    print(f"  Output Order: {fifo_payloads}")
    
    expected_fifo = ["Data Packet 1", "Data Packet 2", "VOIP Packet 1", "Video Packet 1", "VOIP Packet 2"]
    print(f"  Expected Order: {expected_fifo}")

    print("\nTesting Priority Scheduler:")
    priority_output = priority_scheduler(packets_in_arrival_order)
    priority_payloads = [p.payload for p in priority_output]
    print(f"  Output Order: {priority_payloads}")
    
    expected_priority = ["VOIP Packet 1", "VOIP Packet 2", "Video Packet 1", "Data Packet 1", "Data Packet 2"]
    print(f"  Expected Order: {expected_priority}")

