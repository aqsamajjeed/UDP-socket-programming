import socket
from packet import Packet
import random

class UDPClient:
    def __init__(self, ip: str = "127.0.0.1", port: int = 5500, window_size: int = 5, total_packets: int = 20):
        self.ip = ip
        self.port = port
        self.addr = (ip, port)
        self.window_size = window_size
        self.total_packets = total_packets
        self.base = 0
        self.next_seq = 0
        self.dup_ack_count = 0
        self.last_ack = -1
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.settimeout(2)
        print(f"[CLIENT] Starting GBN with window size {window_size}")

    def make_packet(self, seq_no: int, message: str) -> Packet:
        return Packet.create_packet(seq_no, message)


    def run(self):
        while self.base < self.total_packets:
        # Send a window of packets
            window_end = min(self.base + self.window_size, self.total_packets)
            for seq in range(self.base, window_end):
                packet = self.make_packet(seq, f"Packet {seq}")
                if random.random() < 0.1:
                    print(f"[CLIENT] Corrupted for packet {seq}")
                    packet.corrupt()
                else:
                    print(f"[CLIENT] Sending packet {seq}")
                self.client.sendto(packet.packet_data, self.addr) 

            acked_packets = set()

            while len(acked_packets) < (window_end - self.base): 
                try:
                    data, addr = self.client.recvfrom(1024)
                    ack_packet = Packet(packet=data)

                    if ack_packet.get_ack() == 1:
                        seq_no = ack_packet.get_seq_no()
                        if seq_no >= self.base:
                            #print(f"[CLIENT] Received ACK for packet {seq_no}")
                            acked_packets.add(seq_no)
                            if seq_no > self.last_ack:
                                print(f"[CLIENT] Received ACK for packet {seq_no}")
                                self.last_ack = seq_no
                                self.dup_ack_count = 0
                            elif seq_no == self.last_ack:
                                self.dup_ack_count += 1
                                print(f"[CLIENT] Duplicate ACK for {seq_no}")
                        
                                if self.dup_ack_count == 2:
                                    print(f"[CLIENT] Triple duplicate ACKs, fast retransmit for window starting at {self.last_ack+ 1}")
                                    self.dup_ack_count = 0
                                    self.base = self.last_ack + 1
                                    #self.base = self.base + 1 
                                    break

                except socket.timeout:
                    print("[CLIENT] Timeout. Resending window.")
                    self.dup_ack_count = 0
                    self.base = self.last_ack + 1
                    break  

            
            if len(acked_packets) == (window_end - self.base):
                self.base = window_end
                self.next_seq = self.base  



if __name__ == "__main__":
    client = UDPClient()
    client.run()
