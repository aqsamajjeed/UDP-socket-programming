# Reliable UDP Messaging using Go-Back-N Protocol

This project simulates a **reliable data transfer mechanism over UDP** using the **Go-Back-N (GBN)** protocol. Since UDP does not guarantee delivery, order, or integrity, this system implements features to **ensure reliability, error detection, and recovery** — mimicking behavior expected in protocols like TCP.

---

##  Project Structure

| File         | Description                                                             |
|--------------|-------------------------------------------------------------------------|
| `client.py`  | Sends packets to the server using Go-Back-N logic.                      |
| `server.py`  | Receives packets and sends back acknowledgments (ACKs).                 |
| `packet.py`  | Defines packet structure and includes utilities for CRC and corruption. |

---

##  Packet Design

Each packet has a custom header followed by the data payload.

| Field         | Size       | Description                               |
|---------------|------------|-------------------------------------------|
| Sequence No   | 1 byte     | Identifies the packet's order             |
| Checksum      | 4 bytes    | CRC32 checksum for error detection        |
| ACK Flag      | 1 byte     | Indicates whether it's an ACK packet      |
| Data          | Variable   | Actual message content                    |

### Core Packet Functions
- `create_packet()`: Constructs a packet
- `build_packet()`: Builds the byte stream with headers
- `split_packet()`: Parses packet into components
- `verify_crc()`: Checks integrity via checksum
- `corrupt()`: Simulates bit-level corruption
- `get_seq_no()`, `get_ack()`, `get_data()`: Extract individual fields

---

##  Client Logic (`client.py`)

### Key Concepts:
- **Sliding Window**: Uses a `window_size` to control flow
- **Sequence Tracking**: `base` and `next_seq` indicate the sending window
- **Duplicate ACK Detection**: Tracks and counts for fast retransmit

### Simulated Behaviors:
- **Packet Loss**: 10% chance a packet is not sent
- **Packet Corruption**: 10% chance a packet is corrupted
- **Fast Retransmission**: Triggered by three duplicate ACKs
- **Timeout Handling**: Retransmits unacknowledged packets on timeout

---

##  Server Logic (`server.py`)

### Key Concepts:
- **Expected Sequence**: Server waits for specific sequence numbers
- **ACK Strategy**: Sends ACKs for correct packets only

### Simulated Behaviors:
- **ACK Loss/Corruption**: 10% chance to lose or corrupt outgoing ACKs
- **In-order Delivery**: Updates state and sends ACK
- **Out-of-order Handling**: Resends ACK for last correct packet

---

##  Key Features Summary

| Feature                   | Implementation                                                |
|---------------------------|---------------------------------------------------------------|
| Reliable transmission     | GBN with timeouts, cumulative ACKs, fast retransmission       |
| Error detection           | CRC32-based checksum                                          |
| Packet loss simulation    | 10% random drop (client-side)                                 |
| Packet corruption         | 10% random corruption via `corrupt()`                         |
| ACK loss/corruption       | 10% simulated at server                                       |
| Sliding window            | Controlled by `window_size`, `base`, `next_seq`               |
| Timeout + retransmit      | Retransmit on socket timeout                                  |
| Fast retransmission       | Triggered by triple duplicate ACKs                            |

---

##  How to Run

1. Open two terminal windows:
   - One for the server
   - One for the client

2. Start the server:
```bash
python server.py
