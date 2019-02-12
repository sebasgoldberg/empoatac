#!/usr/bin/python
#encoding=utf8

import sys
import os

class QuantidadeAtacadoNaoDefinida(Exception):
    pass

class PluNaoEBase(Exception):
    pass

class PluSoTemUnidadeBase(Exception):
    pass

class RegistroDePrecoNaoEncontrado(Exception):
    pass

TIPO_REG = 1
QUANTIDADE_ATACADO = 26
PLU = 3
PRECO = 4
TIPO_REG_12 = 7
UM = 13
QUANTIDADE_CONTEUDO = 55
PLU_10 = 2
PLU_BASE = 3
PLU_19 = 3
PLU_BASE_19 = 2
PLU_11 = 3
PLU_BASE_11 = 32
PLU_BASE_TEM_FILHOS_11 = 34

BASE_NO_11 = False

EXTENCAO = 'tmp'

class Plus:
    
    def __init__(self):
        
        self.plus = {}
        self.contenedores_por_base = {}

    def add_plu(self, plu):
        
        self.plus[plu.plu] = plu

        if plu.is_base():
            if plu.plu not in self.contenedores_por_base:
                self.contenedores_por_base[plu.plu] = []
            else:
                for contenedor in self.contenedores_por_base[plu.plu]:
                    plu.set_contenedor(contenedor)
        else:

            plu_base = plu.get_plu_base()
            if plu_base not in self.contenedores_por_base:
                self.contenedores_por_base[plu_base] = [ plu ]
            else:
                self.contenedores_por_base[plu_base].append(plu)

            if plu_base in self.plus:
                self.plus[plu_base].set_contenedor(plu)

    def get_plu(self, plu_id):
        return self.plus[plu_id]


class Plu:
    
    def __init__(self, reg_10, plus):
        self.reg_10 = reg_10
        self.plu = self.reg_10[PLU_10]
        self.plus = plus
        self.contenedor = None

    def get_plu_base(self):
        return self.reg_10[PLU_BASE].strip()

    def is_base(self):
        return self.get_plu_base() == ""

    def set_reg_12(self, reg_12):
        self.reg_12 = reg_12

    def set_contenedor(self, plu):
        if self.contenedor is None:
            self.contenedor = plu
        elif self.contenedor.get_quantidade() < plu.get_quantidade():
            self.contenedor = plu

    def get_contenedor(self):
        return self.contenedor

    def get_quantidade(self):
        return int(self.reg_10[QUANTIDADE_CONTEUDO][:-3])

    def get_preco(self):
        try:
            return int(self.reg_12[PRECO])
        except AttributeError:
            print "ERRO: Registro de tipo 12 nao encontrado para PLU %s" % self.plu
            raise RegistroDePrecoNaoEncontrado()

    def get_material(self):
        return self.plu[:-2]

    def tem_contenedor(self):
        return self.contenedor is not None


def get_quantidades_atacado(quan_filename):

    MATERIAL = 0
    QUANTIDADE = 1

    quantidades_atacado = {}

    quan_file = open(quan_filename, 'r')

    try:
        for line in quan_file:
            reg = line.strip().split('\t')
            for i in range(len(reg)):
                reg[i] = reg[i].strip()
            material = reg[MATERIAL]
            quantidade = reg[QUANTIDADE]
            quantidades_atacado[material] = quantidade
    finally:
        quan_file.close()

    return quantidades_atacado


def nova_linea_atacado_12(quantidades_atacado, plu):

    material = plu.get_material()

    if material not in quantidades_atacado:
        raise QuantidadeAtacadoNaoDefinida()

    if not plu.is_base():
        raise PluNaoEBase()

    if not plu.tem_contenedor():
        raise PluSoTemUnidadeBase()
    
    plu_contenedor = plu.get_contenedor()
    quantidade_caixa = plu_contenedor.get_quantidade()
    preco_caixa = plu_contenedor.get_preco() 
    preco_atacado_unidade = preco_caixa / quantidade_caixa
    
    plu.reg_12[PRECO] = str(preco_atacado_unidade).strip().zfill(4)[:-1]+'0'
    plu.reg_12[TIPO_REG_12] = '2'

    return '|'.join(plu.reg_12)


def reg_11_to_atacado(quantidades_atacado, plus, reg):
    plu = plus.get_plu(reg[PLU])
    material = plu.get_material()

    if material not in quantidades_atacado:
        raise QuantidadeAtacadoNaoDefinida()

    if plu.is_base():

        if not plu.tem_contenedor():
            raise PluSoTemUnidadeBase()

        try:
            quantidade_atacado = quantidades_atacado[material]
        except KeyError:
            raise QuantidadeAtacadoNaoDefinida()

        reg[QUANTIDADE_ATACADO] = quantidade_atacado + '000'
        
    return '|'.join(reg)


def convert_emporium_to_emporium_atacado(quantidades_atacado, empo_filename, extencao_novo_arquivo=EXTENCAO):

    empoatac_filename = u'%s.%s' % (empo_filename, extencao_novo_arquivo)

    plus = Plus()

    empo_file = open(empo_filename, 'r')
    empoatac_file = open(empoatac_filename, 'w')

    try:
        
        for line in empo_file:
            reg = line.split('|')
            tipo_reg = reg[TIPO_REG]

            try:

                if tipo_reg in ['11', '12']:
                    plu = plus.get_plu(reg[PLU])
                    if tipo_reg == '12':
                        plu.set_reg_12(reg)
                        if plu.is_base():
                            linea_atacado_12 = nova_linea_atacado_12(quantidades_atacado, plu)
                            empoatac_file.write(line)
                            empoatac_file.write(linea_atacado_12)
                        else:
                            empoatac_file.write(line)
                    else:
                        linea_atacado = reg_11_to_atacado(quantidades_atacado, plus, reg)
                        empoatac_file.write(linea_atacado)
                else:
                    if tipo_reg == '10':
                        plu = Plu(reg, plus)
                        plus.add_plu(plu)

                    empoatac_file.write(line)

            except QuantidadeAtacadoNaoDefinida:
                empoatac_file.write(line)
            except PluSoTemUnidadeBase:
                empoatac_file.write(line)
                print u'WARNING: PLU %s so tem unidade base definida no arquivo de precos. Nao e possivel definir quantidade atacado.' % plu.plu
            except RegistroDePrecoNaoEncontrado:
                empoatac_file.write(line)
                

    finally:
        empo_file.close()
        empoatac_file.close()

def convert_19_to_10_11(empo_filename):

    empo_file = open(empo_filename, 'r')

    lines = []
    plu_base = {}
    plu_base_tem_filhos = {}

    try:

        for line in reversed(empo_file.readlines()):

            reg = line.split('|')
            tipo_reg = reg[TIPO_REG]

            if tipo_reg == '10':
                try:
                    reg[PLU_BASE] = plu_base[reg[PLU_10]]
                except KeyError:
                    pass
                lines.append('|'.join(reg))
            elif BASE_NO_11 and tipo_reg == '11':
                try:
                    reg[PLU_BASE_11] = plu_base[reg[PLU_11]]
                except KeyError:
                    try:
                        if plu_base_tem_filhos[reg[PLU_11]] == True:
                            reg[PLU_BASE_TEM_FILHOS_11] = '1'
                    except KeyError:
                        pass
                lines.append('|'.join(reg))
            elif tipo_reg == '19':
                plu_base[reg[PLU_19]] = reg[PLU_BASE_19]
                plu_base_tem_filhos[reg[PLU_BASE_19]] = True
                lines.append(line)
            else:
                lines.append(line)

    finally:
        empo_file.close()

    # Criamos o novo arquivo com o PLU base dos registros 10 preenchidos.

    empo19to10_filename = u'%s.%s' % (empo_filename, EXTENCAO)

    empo19to10_file = open(empo19to10_filename, 'w')

    for line in reversed(lines):
        empo19to10_file.write(line)

    empo19to10_file.close()

    os.rename(empo19to10_filename, empo_filename )


def remove_plu_base_10(empo_filename):

    empo_sem_plu_base_10_filename = u'%s.%s' % (empo_filename, EXTENCAO)

    empo_file = open(empo_filename, 'r')
    empo_sem_plu_base_10_file = open(empo_sem_plu_base_10_filename, 'w')

    try:

        for line in empo_file:

            reg = line.split('|')
            tipo_reg = reg[TIPO_REG]

            if tipo_reg == '10':
                reg[PLU_BASE] = ' '
                empo_sem_plu_base_10_file.write('|'.join(reg))
            else:
                empo_sem_plu_base_10_file.write(line)

    finally:
        empo_file.close()
        empo_sem_plu_base_10_file.close()

    os.rename(empo_sem_plu_base_10_filename, empo_filename )


def empoatac(quan_filename, empo_filenames, mudar_original=False, fix_base_no_10=False):

    quantidades_atacado = get_quantidades_atacado(quan_filename)

    for empo_filename in empo_filenames:
        if fix_base_no_10:
            convert_19_to_10_11(
                empo_filename
            )
        convert_emporium_to_emporium_atacado(
            quantidades_atacado,
            empo_filename,
            )
        if mudar_original:
            os.rename('%s.%s' % (empo_filename, EXTENCAO), empo_filename )
        if fix_base_no_10:
            remove_plu_base_10(
                empo_filename
            )

if __name__ == '__main__':
    if sys.argv[2] == '--BASE_NO_11':
        BASE_NO_11 = True
        index_argv_files = 3
    else:
        index_argv_files = 2

    empoatac(sys.argv[1], sys.argv[index_argv_files:], mudar_original=True, fix_base_no_10=True)
