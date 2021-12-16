import abc
from typing import TextIO, Dict, List, Optional, Tuple
from collections import namedtuple, defaultdict
import sys

LITERAL_PACKET_TYPE_ID = 4

class Packet(object):
    def __init__(self, version: int, type_id: int):
        self.version = version
        self.type_id = type_id

class LiteralPacket(Packet):
    def __init__(self, version: int, value: int):
        super().__init__(version, LITERAL_PACKET_TYPE_ID)
        self.value = value
    
    def __str__(self):
        return f'Literal<{self.version}, {self.type_id}, {self.value}>'

class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, subpackets: List[Packet]):
        super().__init__(version, type_id)
        self.subpackets = subpackets
    
    def __str__(self):
        out = f'Operator<{self.version}, {self.type_id}>\n'

        for packet in self.subpackets:
            out += f'{packet}\n'

        return out


def read_input(textio: TextIO) -> str:
    out = ""
    line = textio.readline().strip()

    for char in line:
        out += bin(int(char, 16))[2:].zfill(4)
    return out

def decode_packet_header(first):
    return int(first[0:3], 2), int(first[3:6], 2), 6

def decode_literal(version: int, stream: str):
    offset = 0
    nibbles = []
    while True:
        is_last = stream[offset] == '0'
        nibbles.append(int(stream[offset+1:offset+5], 2))
        offset += 5
        if is_last:
            break

    literal = 0
    for i in range(len(nibbles)):
        literal += nibbles[i]<<((len(nibbles)-i-1)*4)

    # print(f'nibbles: {nibbles} = {literal}')

    return LiteralPacket(version, literal), offset

def decode_operator_packet(version: int, type_id: int, stream: str):
    packets = []
    if stream[0] == '0':
        consumed = 16
        subpacket_length = int(stream[1:16], 2)
        # print(f'op length: {subpacket_length}')
        while subpacket_length > 0:
            packet, new_consumed = decode_packet(stream[consumed:])
            # print(packet, new_consumed)
            consumed += new_consumed
            subpacket_length -= new_consumed
            packets.append(packet)
    elif stream[0] == '1':
        consumed = 12
        subpacket_count = int(stream[1:12], 2)
        # print(f'op count: {subpacket_count}')
        for _ in range(subpacket_count):
            packet, new_consumed = decode_packet(stream[consumed:])
            consumed += new_consumed
            packets.append(packet)
    else:
        raise Exception(stream[0])
    
    return OperatorPacket(version, type_id, packets), consumed

def decode_packet(transmission: str):
    consumed = 0
    version, type_id, new_consumed = decode_packet_header(transmission)
    consumed += new_consumed
    # print(version, type_id, consumed)

    if type_id == LITERAL_PACKET_TYPE_ID:
        packet, new_consumed = decode_literal(version, transmission[consumed:])
        # print(f'read literal "{literal}" with {consumed} bits')
        consumed += new_consumed
    else:  
        packet, new_consumed = decode_operator_packet(version, type_id, transmission[consumed:])
        consumed += new_consumed

    return packet, consumed


transmission = read_input(sys.stdin)
print(transmission)
packets, consumed = decode_packet(transmission)
print(packets)