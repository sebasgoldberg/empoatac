#!/usr/bin/python
#encoding=utf8

import empoatac
import unittest
import filecmp
import os

class EmpoAtacTestCase(unittest.TestCase):

    def test_empoatac(self):

        loja999 = 'testdata/loja999'
        loja999_new = 'testdata/loja999.tmp'
        loja999_new_expected = 'testdata/loja999.expected'

        try:
            os.remove(loja999_new)
        except OSError:
            pass
        
        empoatac.empoatac('testdata/quantidades_atacado.txt', [loja999])

        self.assertTrue(filecmp.cmp(loja999_new, loja999_new_expected))

        os.remove(loja999_new)

    def test_mesmo_arquivo(self):

        loja999 = 'testdata/loja999'
        loja999_new = 'testdata/loja999.tmp'

        try:
            os.remove(loja999_new)
        except OSError:
            pass
        
        empoatac.empoatac('testdata/vazio.txt', [loja999])

        self.assertTrue(filecmp.cmp(loja999_new, loja999))

        os.remove(loja999_new)

    def test_multiplos_materiais(self):

        loja801 = 'testdata/loja801'
        loja801_new = 'testdata/loja801.tmp'
        loja801_new_expected = 'testdata/loja801.expected'

        try:
            os.remove(loja801_new)
        except OSError:
            pass
        
        empoatac.empoatac('testdata/quantidades_atacado.txt', [loja801])

        self.assertTrue(filecmp.cmp(loja801_new, loja801_new_expected))

        os.remove(loja801_new)

    def test_multiplos_embalagens(self):

        grande = 'testdata/grande'
        grande_new = 'testdata/grande.tmp'
        grande_expected = 'testdata/grande.expected'

        try:
            os.remove(grande_new)
        except OSError:
            pass
        
        empoatac.empoatac('testdata/quantidades_atacado.txt', [grande])

        self.assertTrue(filecmp.cmp(grande_new, grande_expected))

        os.remove(grande_new)

    def test_muito_grande(self):

        muito_grande = 'testdata/muito_grande'
        muito_grande_new = 'testdata/muito_grande.tmp'

        try:
            os.remove(muito_grande_new)
        except OSError:
            pass
        
        empoatac.empoatac('testdata/QtdAtacadoTeste.txt', [muito_grande])

        os.remove(muito_grande_new)



if __name__ == '__main__':
    unittest.main()
