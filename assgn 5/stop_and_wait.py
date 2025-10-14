import random
import time

def simulate_network(packet, loss_prob):
    if random.random() < loss_prob:
        return None
    return packet

def sender(data_frames, loss_prob, timeout_duration):
    seq_num = 0
    frame_index = 0
    
    while frame_index < len(data_frames):
        frame_to_send = {'seq': seq_num, 'data': data_frames[frame_index]}
        
        while True:
            print(f"Sending Frame {frame_index} (seq: {seq_num})")
            
            received_by_receiver = simulate_network(frame_to_send, loss_prob)
            ack = None
            if received_by_receiver:
                ack = receiver(received_by_receiver, seq_num)
                ack = simulate_network(ack, loss_prob)

            start_time = time.time()
            ack_is_correct = False
            while time.time() - start_time < timeout_duration:
                if ack and ack['ack_num'] == seq_num:
                    ack_is_correct = True
                    break
            
            if ack_is_correct:
                print(f"ACK {seq_num} received for Frame {frame_index}")
                frame_index += 1
                seq_num = 1 - seq_num
                break
            else:
                print(f"Timeout! Frame {frame_index} lost, retransmitting...")

def receiver(received_frame, expected_seq_num):
    if received_frame['seq'] == expected_seq_num:
        return {'ack_num': expected_seq_num}
    else:
        return None

if __name__ == "__main__":
    TOTAL_FRAMES = 5
    LOSS_PROBABILITY = 0.3
    TIMEOUT = 1.0

    frames = [f"Data-{i}" for i in range(TOTAL_FRAMES)]
    sender(frames, LOSS_PROBABILITY, TIMEOUT)
    print("\nAll frames have been successfully transmitted.")
