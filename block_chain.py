#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib, datetime


class Chain():
    
    def __init__(self):
        self.blocks = [Block(0, 'init_data', 'init_hash')]
    
    def add_block(self, data):
        self.blocks.append(Block(len(self.blocks),
                                 data,
                                 self.blocks[-1].hash))
    
    def verify(self):
        for i in range(1, len(self.blocks)):
            if self.blocks[i].verify() and \
                self.blocks[i].index == i and \
                self.blocks[i-1].timestamp >= self.blocks[i].timestamp and \
                self.blocks[i-1].hash == self.blocks[i].previous_hash and \
                self.blocks[i].hash == self.blocks[i].hashing():
                    return True
            else:
                return False        

class Block():
    
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = datetime.datetime.utcnow()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()
    
    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()
    
    def verify(self):
        instances = [self.index, self.timestamp, self.previous_hash, self.hash]
        types = [int, datetime.datetime, str, str]
        if sum(map(lambda inst_, type_: isinstance(inst_, type_), instances, types)) == len(instances):
            return True
        else:
            return False
