import matplotlib.pyplot as plt

def simulate_tcp_congestion_control(total_rounds, initial_ssthresh, loss_round):
    cwnd = 1
    ssthresh = initial_ssthresh
    cwnd_history = []
    
    print("Round |   Phase            | CWND | SSTHRESH")
    print("------------------------------------------------")

    for round_num in range(1, total_rounds + 1):
        cwnd_history.append(cwnd)
        
        if round_num == loss_round:
            phase = "Packet Loss!"
            print(f"{round_num:<5} | {phase:<18} | {cwnd:<4} | {ssthresh:<8}")
            ssthresh = cwnd // 2
            cwnd = 1
            continue

        if cwnd < ssthresh:
            phase = "Slow Start"
            cwnd *= 2
        else:
            phase = "Congestion Avoidance"
            cwnd += 1
            
        print(f"{round_num:<5} | {phase:<18} | {cwnd:<4} | {ssthresh:<8}")
        
    return cwnd_history

def plot_cwnd(rounds, cwnd_data):
    plt.figure(figsize=(12, 6))
    plt.plot(rounds, cwnd_data, marker='o', linestyle='-', label='cwnd')
    plt.title('TCP Congestion Window (cwnd) Simulation')
    plt.xlabel('Transmission Round')
    plt.ylabel('Congestion Window Size (MSS)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rounds)
    
    plt.savefig('cwnd_plot.png')
    print("\nPlot saved to cwnd_plot.png")
    plt.show()

if __name__ == "__main__":
    TOTAL_ROUNDS = 20
    INITIAL_SSTHRESH = 16
    PACKET_LOSS_ROUND = 12

    history = simulate_tcp_congestion_control(TOTAL_ROUNDS, INITIAL_SSTHRESH, PACKET_LOSS_ROUND)
    
    rounds = list(range(1, TOTAL_ROUNDS + 1))
    plot_cwnd(rounds, history)
