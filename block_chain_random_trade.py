#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from block_chain import Chain
import random


class RandomTrade():
    
    def __init__(self):
        self.persons = ['p1', 'p2', 'p3']
        self.market = {'600600':50.0, '600519':1000.0, '000568':100.0}
        self.dict_data = {'p1':{'stocks':{'600600':10000}, 'money':500000.0},
                          'p2':{'stocks':{'600519':1000}, 'money':0.0},
                          'p3':{'stocks':{'000568':5000}, 'money':500000.0}}
        self.chain = Chain()
    
    def __call__(self, trade_num):
        for _ in range(trade_num):
            p_rand = random.sample(self.persons, 3)
            seller, buyers, stock_trade, buys = self.random_trade(self.dict_data[p_rand[0]])
            self.chain.add_block({'seller':seller, 'buyers':buyers, 'stock_trade':stock_trade, \
                             'buys':buys, 'dict_data':self.dict_data})
    
    def random_trade(self, p_data):
        rand_ps = random.sample(self.persons, 3)
        seller = self.dict_data[rand_ps[0]]
        buyers = []
        for rpi in rand_ps[1:]:
            buyers.append(self.dict_data[rpi])
        max_v = max(seller['stocks'].values())
        if max_v < 1:
            return None, None, None, None
        for (key, value) in seller['stocks'].items():
            if value == max_v:
                stock_trade = key
                break
        vol = 0
        while vol < 100:
            vol, chg = round(random.randint(100, max_v), -2), (random.random() - 0.5) / 5
        self.market[stock_trade] *= (1.0 + chg)
        ask = []
        sold_out = False
        for _ in range(len(buyers)):
            if sold_out:
                ask.append(0.0)
            else:
                vi = round(random.randint(100, vol), -2)
                if vi + sum(ask) >= vol:
                    ask.append(vol - sum(ask))
                    sold_out = True
                else:
                    ask.append(vi)
        
        buys = []
        for bi, vi in zip(buyers, ask):
            if vi > 0:
                if bi['money'] >= self.market[stock_trade] * vi:
                    vim = vi
                else:
                    max_v = bi['money'] / self.market[stock_trade]
                    vim = max_v - max_v % 100
                buys.append(vim)
                bi['money'] -= self.market[stock_trade] * vim
                try:
                    bi['stocks'][stock_trade] += vim
                except:
                    bi['stocks'][stock_trade] = vim
            else:
                buys.append(0.0)
        buys_sum = sum(buys)
        seller['stocks'][stock_trade] -= buys_sum
        seller['money'] += self.market[stock_trade] * buys_sum
        
        return seller, buyers, stock_trade, buys


r = RandomTrade()
r(15)
          


