#!/usr/bin/python
#encoding=utf8

# @todo: Lógica pra procesar material con N UMs (tomar mayor cantidad para calcular precio)
import sys

class QuantidadeAtacadoNaoDefinida(Exception):
    pass

class PluNaoEBase(Exception):
    pass

def get_quantidades_atacado(quan_filename):

    MATERIAL = 0
    QUANTIDADE = 1

    quantidades_atacado = {}

    with open(quan_filename, 'r') as quan_file:
        for line in quan_file:
            reg = line.strip().split('\t')
            for i in range(len(reg)):
                reg[i] = reg[i].strip()
            # @todo Verificar si tem loja
            #loja = reg[LOJA]
            material = reg[MATERIAL]
            quantidade = reg[QUANTIDADE]
            """
            if loja not in quantidades_atacado:
                quantidades_atacado[loja] = {material: quantidade}
            else:
                quantidades_atacado[loja][material] = quantidade
                """
            quantidades_atacado[material] = quantidade

    return quantidades_atacado


TIPO_REG = 1
QUANTIDADE_ATACADO = 26
PLU = 3
PRECO = 4
TIPO_REG_12 = 7
UM = 13
QUANTIDADE_CAIXA = 55
PLU_10 = 2
PLU_BASE = 3

def get_material_plu(plu):
    return plu[:-2]

def get_um_plu(plu):
    return plu[-2:]

def reg_to_linea_atacado(quantidades_atacado, plus, reg):
    plu = plus.get_plu(reg[PLU])
    material = get_material_plu(plu.plu)

    if plu.is_base():
        try:
            quantidade_atacado = quantidades_atacado[material] 
        except KeyError:
            raise QuantidadeAtacadoNaoDefinida()

        reg[QUANTIDADE_ATACADO] = quantidade_atacado
        
    return '|'.join(reg)


def get_quantidade_caixa():
    raise Exception(u'Ainda não definido de onde obter as quantidades das caixas dos produtos.')

def nova_linea_atacado_12(quantidades_atacado, plu):

    if not plu.is_base():
        raise PluNaoEBase()

    material = get_material_plu(plu.plu)

    if material not in quantidades_atacado:
        raise QuantidadeAtacadoNaoDefinida()
    
    plu_contenedor = plu.get_contenedor()
    quantidade_caixa = plu_contenedor.get_quantidade()
    preco_caixa = plu_contenedor.get_preco() 
    preco_atacado_unidade = preco_caixa / quantidade_caixa
    
    plu.reg_12[PRECO] = str(preco_atacado_unidade).strip()
    plu.reg_12[TIPO_REG_12] = '2'

    return '|'.join(plu.reg_12)

class Plus():
    
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
                self.plus[plu_base].set_contenedor(plu)

    def get_plu(self, plu_id):
        return self.plus[plu_id]


class Plu():
    
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
        elif self.contenedor.get_quantidade_conteudo() < plu.get_quantidade_conteudo():
            self.contenedor = plu

    def get_contenedor(self):
        return self.contenedor

    def get_quantidade(self):
        return int(self.reg_10[QUANTIDADE_CAIXA][:-3])

    def get_preco(self):
        return int(self.reg_12[PRECO])

def convert_emporium_to_emporium_atacado(quantidades_atacado, empo_filename, extencao_novo_arquivo='new'):
    
    empoatac_filename = u'%s.%s' % (empo_filename, extencao_novo_arquivo)

    plus = Plus()

    with open(empo_filename, 'r') as empo_file, open(empoatac_filename, 'w') as empoatac_file:
        
        for line in empo_file:
            reg = line.split('|')
            tipo_reg = reg[TIPO_REG]

            try:

                if tipo_reg in ['11', '12']:
                    if tipo_reg == '12':
                        plu = plus.get_plu(reg[PLU])
                        plu.set_reg_12(reg)
                        if plu.is_base():
                            linea_atacado_12 = nova_linea_atacado_12(quantidades_atacado, plu)
                            empoatac_file.write(line)
                            empoatac_file.write(linea_atacado_12)
                        else:
                            empoatac_file.write(line)
                    else:
                        linea_atacado = reg_to_linea_atacado(quantidades_atacado, plus, reg)
                        empoatac_file.write(linea_atacado)
                else:
                    if tipo_reg == '10':
                        plu = Plu(reg, plus)
                        plus.add_plu(plu)

                    empoatac_file.write(line)

            except QuantidadeAtacadoNaoDefinida:
                empoatac_file.write(line)


def empoatac(quan_filename, empo_filenames):

    quantidades_atacado = get_quantidades_atacado(quan_filename)

    for empo_filename in empo_filenames:
        convert_emporium_to_emporium_atacado(
            quantidades_atacado,
            empo_filename,
            'new'
            )

if __name__ == '__main__':
    empoatac(sys.argv[1], sys.argv[2:])
