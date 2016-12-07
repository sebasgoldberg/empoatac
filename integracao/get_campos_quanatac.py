#!/usr/bin/python
#encoding=utf8

import sys

TIPO_REG=1

BASE_PLU_KEY=3

WHOLESALE_QUANTITY=26

PRICE=4

TYPE_PRICE=7

for filename in sys.argv[1:]:
    print(u'-------------- %s -----------------' % filename)
    with open(filename,'r') as f:
        for line in f:
            reg = line.split('|')
            tipo_reg = reg[TIPO_REG]
            if tipo_reg == '10':
                print('REG %s: %s' % (tipo_reg, reg))
                print('GRUP_ATAC (REG 10, campo 4: base_plu_key): %s' % reg[BASE_PLU_KEY])
            elif tipo_reg == '11':
                print('REG %s: %s' % (tipo_reg, reg))
                print('QUAN_ATAC (REG 11, campo 27: wholesale_quantity): %s' % reg[WHOLESALE_QUANTITY])
            elif tipo_reg == '12':
                print('REG %s: %s' % (tipo_reg, reg))
                print('PRECO_ATAC (REG 12, campo 5: Price): %s' % reg[PRICE])
                print('TYPE_PRICE (REG 12, campo 8: type_price): %s' % reg[TYPE_PRICE])


