import socket
from packet import Packet
import random 

class UDPServer:
    def __init__(self, ip: str = "127.0.0.1", port: int = 5500):
        self.ip = ip
        self.port = port
        self.addr = (ip, port)
        self.expected_seq = 0
        self.last_ack = -1
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(self.addr)
        print(f"[SERVER] Listening on {ip}:{port}")

    def make_ack_packet(self, seq_no: int):
        return Packet.create_packet(seq_no, "ACK", ack=1)

    def _check_crc(self, packet: Packet) -> bool:
        return packet.verify_crc()

    def run(self):
        while True:
            data, addr = self.server.recvfrom(1024)
            packet = Packet(packet=data)

            # Optional: simulate packet loss/corruption
            if random.random() < 0.1:
                print(f"[SERVER] Simulating drop for packet {packet.get_seq_no()}")
                continue
            

            if not self._check_crc(packet):
                if self.last_ack == -1: 
                    continue
                else:
                    print(f"[SERVER] Corrupted packet {packet.get_seq_no()}, sending ACK for {self.last_ack}")
                    ack_packet = self.make_ack_packet(self.last_ack)
                    self.server.sendto(ack_packet.packet_data, addr)
                    continue

            seq_no = packet.get_seq_no()

            if seq_no == self.expected_seq:
                print(f"[SERVER] Received expected packet {seq_no}")
                self.expected_seq += 1
                self.last_ack = seq_no
            else:
                print(f"[SERVER] Received out-of-order packet {seq_no} (expected {self.expected_seq})")

            ack_packet = self.make_ack_packet(self.last_ack)
            self.server.sendto(ack_packet.packet_data, addr) 
            print(f"[SERVER] Sent ACK for packet {self.last_ack}")

        
if __name__ == "__main__":
    server = UDPServer()
    server.run()
