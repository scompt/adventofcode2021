from abc import ABC, abstractmethod
from typing import TextIO, Dict, List, Optional, Tuple
from collections import namedtuple, defaultdict
import sys
import functools
import operator
from enum import Enum

class PacketTypeId(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL = 7

class Packet(ABC):
    def __init__(self, version: int, type_id: int):
        self.version = version
        self.type_id = type_id
    
    @abstractmethod
    def value(self):
        pass

class LiteralPacket(Packet):
    def __init__(self, version: int, literal: int):
        super().__init__(version, PacketTypeId.LITERAL.value)
        self.literal = literal
    
    def value(self) -> int:
        return self.literal

    def __str__(self) -> str:
        return f'Literal<{self.version}, {self.type_id}, {self.literal}>'

class OperatorPacket(Packet):
    def __init__(self, version: int, type_id: int, subpackets: List[Packet]):
        super().__init__(version, type_id)
        self.subpackets = subpackets
    
    def value(self) -> int:
        if self.type_id == PacketTypeId.SUM.value:
            return sum(p.value() for p in self.subpackets)

        elif self.type_id == PacketTypeId.PRODUCT.value:
            return functools.reduce(operator.mul, [p.value() for p in self.subpackets])

        elif self.type_id == PacketTypeId.MINIMUM.value:
            return min(p.value() for p in self.subpackets)

        elif self.type_id == PacketTypeId.MAXIMUM.value:
            return max(p.value() for p in self.subpackets)

        elif self.type_id == PacketTypeId.GREATER_THAN.value:
            if self.subpackets[0].value() > self.subpackets[1].value():
                return 1
            else:
                return 0

        elif self.type_id == PacketTypeId.LESS_THAN.value:
            if self.subpackets[0].value() < self.subpackets[1].value():
                return 1
            else:
                return 0

        elif self.type_id == PacketTypeId.EQUAL.value:
            if self.subpackets[0].value() == self.subpackets[1].value():
                return 1
            else:
                return 0

        else:
            raise Exception(self.type_id)

    def __str__(self) -> str:
        out = f'Operator<{self.version}, {self.type_id}>\n'

        for packet in self.subpackets:
            out += f'{packet}\n'

        return out


def read_input(textio: TextIO) -> str:
    for line in textio.readlines():
        out = ""
        line = line.strip()

        for char in line:
            out += bin(int(char, 16))[2:].zfill(4)
        yield out

def decode_packet_header(first):
    return int(first[0:3], 2), int(first[3:6], 2), 6

def decode_literal(version: int, stream: str) -> LiteralPacket:
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

def decode_operator_packet(version: int, type_id: int, stream: str) -> OperatorPacket:
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

def decode_packet(transmission: str) -> Packet:
    consumed = 0
    version, type_id, new_consumed = decode_packet_header(transmission)
    consumed += new_consumed
    # print(version, type_id, consumed)

    if type_id == PacketTypeId.LITERAL.value:
        packet, new_consumed = decode_literal(version, transmission[consumed:])
        # print(f'read literal "{literal}" with {consumed} bits')
        consumed += new_consumed
    else:  
        packet, new_consumed = decode_operator_packet(version, type_id, transmission[consumed:])
        consumed += new_consumed

    return packet, consumed

for transmission in read_input(sys.stdin):
    print(transmission)
    packet, consumed = decode_packet(transmission)
    print(packet.value())