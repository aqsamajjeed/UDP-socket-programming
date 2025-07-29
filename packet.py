import zlib

class Packet:
    def __init__(self, seq_no=None, data=None, packet=None, ack=0):
        if packet is not None:
            self.packet_data = packet
            self._split_packet()
        else:
            self.seq_no = seq_no
            self.data = data
            self.crc = self._calculate_crc32(data)
            self.ack = ack
            self.corrupted = 0
            self.packet_data = self._build_packet()

    def _calculate_crc32(self, data: bytes) -> int:
        return zlib.crc32(data)

    def _build_packet(self) -> bytes:
        seq_no_bytes = self.seq_no.to_bytes(1, 'big')
        crc_bytes = self.crc.to_bytes(4, 'big')
        ack_flag = self.ack.to_bytes(1, 'big')
        return seq_no_bytes + crc_bytes + ack_flag + self.data

    def _split_packet(self):
        self.seq_no = self.packet_data[0]
        self.crc = int.from_bytes(self.packet_data[1:5], 'big')
        self.ack = self.packet_data[5]
        self.data = self.packet_data[6:]

    def verify_crc(self) -> bool:
        calculated_crc = self._calculate_crc32(self.data)
        return self.crc == calculated_crc

    def get_data(self) -> str:
        return self.data.decode()

    def get_seq_no(self) -> int:
        return self.seq_no

    def get_ack(self) -> int:
        return self.ack

    def corrupt(self):
        corrupted_crc = (self.crc + 1).to_bytes(4, 'big')
        self.packet_data = self.packet_data[0:1] + corrupted_crc + self.packet_data[5:]
        self._split_packet()

    @staticmethod
    def create_packet(seq_no: int, message: str, ack=0) -> 'Packet':
        data = message.encode()
        return Packet(seq_no=seq_no, data=data, ack=ack)
