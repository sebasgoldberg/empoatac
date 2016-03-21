#!/usr/bin/python
#encoding=utf8

import empoatac
import unittest
import filecmp
import os

class EmpoAtacTestCase(unittest.TestCase):

    def test_empoatac(self):

        loja999 = 'testdata/loja999'
        loja999_new = 'testdata/loja999.new'
        loja999_new_expected = 'testdata/loja999.new.expected'

        try:
            os.remove(loja999_new)
        except OSError:
            pass
        
        empoatac.empoatac('testdata/quantidades_atacado.txt', [loja999])

        self.assertTrue(filecmp.cmp(loja999_new, loja999_new_expected))

        os.remove(loja999_new)


if __name__ == '__main__':
    unittest.main()
