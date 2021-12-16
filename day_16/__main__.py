from abc import ABC, abstractmethod
from typing import TextIO, Dict, List, Optional, Tuple
from collections import namedtuple, defaultdict
import sys
import functools
import operator
from enum import Enum
from utils import lookahead

class PacketTypeId(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL = 7

class OperatorStyle(Enum):
    LENGTH = '0'
    COUNT = '1'

class Packet(ABC):
    @classmethod
    def decode(cls, transmission: str) -> "Packet":
        version = int(transmission[0:3], 2)
        type_id = int(transmission[3:6], 2)
        consumed = 6

        if type_id == PacketTypeId.LITERAL.value:
            packet, new_consumed = LiteralPacket.decode(version, transmission[consumed:])
            consumed += new_consumed
        else:  
            packet, new_consumed = OperatorPacket.decode(version, type_id, transmission[consumed:])
            consumed += new_consumed

        return packet, consumed

    def __init__(self, version: int, type_id: PacketTypeId):
        self.version = version
        self.type_id = type_id
    
    @abstractmethod
    def value(self) -> int:
        pass

    def encode(self) -> str:
        header = bin(self.version)[2:].zfill(3) + bin(self.type_id.value)[2:].zfill(3)
        contents = self.encode_contents()
        return header + contents
    
    @abstractmethod
    def encode_contents(self) -> str:
        pass


class LiteralPacket(Packet):
    @classmethod
    def decode(cls, version: int, stream: str) -> "LiteralPacket":
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

        return LiteralPacket(version, literal), offset

    def __init__(self, version: int, literal: int):
        super().__init__(version, PacketTypeId.LITERAL)
        self.literal = literal
    
    def value(self) -> int:
        return self.literal

    def encode_contents(self) -> str:
        outs = []
        value = self.literal
        while value:
            outs.append(bin(value & 15)[2:].zfill(4))
            value = value >> 4

        out = ''
        for digit, more in lookahead(outs[::-1]):
            if more:
                out += '1'
            else:
                out += '0'
            out += digit

        return out

    def __str__(self) -> str:
        return f'Literal<{self.version}, {self.type_id}, {self.literal}>'

class OperatorPacket(Packet):

    @classmethod
    def decode(cls, version: int, type_id: PacketTypeId, stream: str) -> "OperatorPacket":
        packets = []
        style = None
        if stream[0] == OperatorStyle.LENGTH.value:
            style = OperatorStyle.LENGTH
            consumed = 16
            subpacket_length = int(stream[1:16], 2)

            while subpacket_length > 0:
                packet, new_consumed = Packet.decode(stream[consumed:])
                consumed += new_consumed
                subpacket_length -= new_consumed
                packets.append(packet)
        elif stream[0] == OperatorStyle.COUNT.value:
            style = OperatorStyle.COUNT
            consumed = 12
            subpacket_count = int(stream[1:12], 2)
            for _ in range(subpacket_count):
                packet, new_consumed = Packet.decode(stream[consumed:])
                consumed += new_consumed
                packets.append(packet)
        else:
            raise Exception(stream[0])
        
        return OperatorPacket(version, PacketTypeId(type_id), style, packets), consumed

    def __init__(self, version: int, type_id: int, style: OperatorStyle, subpackets: List[Packet]):
        super().__init__(version, type_id)
        self.style = style
        self.subpackets = subpackets
    
    def value(self) -> int:
        if self.type_id == PacketTypeId.SUM:
            return sum(p.value() for p in self.subpackets)

        elif self.type_id == PacketTypeId.PRODUCT:
            return functools.reduce(operator.mul, [p.value() for p in self.subpackets])

        elif self.type_id == PacketTypeId.MINIMUM:
            return min(p.value() for p in self.subpackets)

        elif self.type_id == PacketTypeId.MAXIMUM:
            return max(p.value() for p in self.subpackets)

        elif self.type_id == PacketTypeId.GREATER_THAN:
            if self.subpackets[0].value() > self.subpackets[1].value():
                return 1
            else:
                return 0

        elif self.type_id == PacketTypeId.LESS_THAN:
            if self.subpackets[0].value() < self.subpackets[1].value():
                return 1
            else:
                return 0

        elif self.type_id == PacketTypeId.EQUAL:
            if self.subpackets[0].value() == self.subpackets[1].value():
                return 1
            else:
                return 0

        else:
            raise Exception(self.type_id)

    def encode_contents(self) -> str:
        out = ''
        for packet in self.subpackets:
            out += packet.encode()

        if self.style == OperatorStyle.LENGTH:
            out = self.style.value + bin(len(out))[2:].zfill(15) + out
        
        elif self.style == OperatorStyle.COUNT:
            out = self.style.value + bin(len(self.subpackets))[2:].zfill(11) + out

        return out

    def __str__(self) -> str:
        out = f'Operator<{self.version}, {self.type_id}>\n'

        for packet in self.subpackets:
            for line in str(packet).split('\n'):
                out += f'  {line}\n'

        return out[:-1]


def read_input(textio: TextIO) -> str:
    for line in textio.readlines():
        out = ""
        line = line.strip()

        for char in line:
            out += bin(int(char, 16))[2:].zfill(4)
        yield out

for transmission in read_input(sys.stdin):
    # print(transmission, len(transmission))
    packet, consumed = Packet.decode(transmission)
    
    # encoded = packet.encode()
    # encoded += '0' * (8-((len(encoded)) % 8))
    # print(encoded, len(encoded))
    print(packet.value())
    # print(packet)