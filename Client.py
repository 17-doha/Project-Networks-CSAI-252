import socket as s


def acknowledgement(packet):
    packet_id = packet[0:16]
    file_id = packet[16:32]
    message = packet[32:-32]
    Trailer = packet[-32:]
    return packet_id, file_id, Trailer



s2 = s.socket(s.AF_INET, s.SOCK_DGRAM)
port = 12345
address = ('127.0.0.1', port)
s2.bind(address)

expected_packet_num = 0

while True:
    data, server = s2.recvfrom(4096)
    packet_id, file_id, Trailer = acknowledgement(data.decode())

    if packet_id == expected_packet_num:
        print(f'Packet {expected_packet_num} received correctly')
        expected_packet_num += 1
    else:
        print(f'Packet {packet_id} received out of order')

    # Send acknowledgment for the last correctly received packet
    ack_message = f"{expected_packet_num - 1}"
    s2.sendto(ack_message.encode(), server)

    if Trailer == '1111111111111111':
        print(f'Last packet received: {data.decode()}')
        break

s2.close()
