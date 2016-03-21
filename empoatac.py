#!/usr/bin/python
#encoding=utf8


class QuantidadeAtacadoNaoDefinida(Exception):
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


def get_material_plu(plu):
    return plu[:-2]

def get_um_plu(plu):
    return plu[-2:]

def reg_to_linea_atacado(quantidades_atacado, reg):
    tipo_reg = reg[TIPO_REG]
    plu = reg[PLU]
    material = get_material_plu(plu)
    um = get_um_plu(plu)

    if um == '00':
        try:
            quantidade_atacado = quantidades_atacado[material] 
        except KeyError:
            raise QuantidadeAtacadoNaoDefinida()

        reg[QUANTIDADE_ATACADO] = quantidade_atacado
        
    return '|'.join(reg)


def get_quantidade_caixa():
    raise Exception(u'Ainda não definido de onde obter as quantidades das caixas dos produtos.')

def nova_linea_atacado_12(quantidades_atacado, reg_12_unidade, reg_12_caixa, reg_10_caixa):
    
    quantidade_caixa = int(reg_10_caixa[QUANTIDADE_CAIXA][:-3])
    preco_caixa = int(reg_12_caixa[PRECO])
    preco_atacado_unidade = preco_caixa / quantidade_caixa
    
    reg_12_unidade[PRECO] = str(preco_atacado_unidade).strip()
    reg_12_unidade[TIPO_REG_12] = '2'

    return '|'.join(reg_12_unidade)


def convert_emporium_to_emporium_atacado(quantidades_atacado, empo_filename, extencao_novo_arquivo='new'):
    
    empoatac_filename = u'%s.%s' % (empo_filename, extencao_novo_arquivo)

    with open(empo_filename, 'r') as empo_file, open(empoatac_filename, 'w') as empoatac_file:
        
        reg_10_caixa = None
        reg_12_unidade = None
        reg_12_caixa = None
        tipo_reg_anterior = None

        for line in empo_file:
            reg = line.split('|')
            tipo_reg = reg[TIPO_REG]

            try:

                if tipo_reg in ['11', '12']:
                    if tipo_reg == '12':
                        um_plu = get_um_plu(reg[PLU])
                        if um_plu == '00':
                            reg_12_unidade = reg
                        elif um_plu == '01':
                            reg_12_caixa = reg
                        empoatac_file.write(line)
                    else:
                        linea_atacado = reg_to_linea_atacado(quantidades_atacado, reg)
                        empoatac_file.write(linea_atacado)
                else:
                    if tipo_reg == '10' and reg[UM] == 'CX':
                        reg_10_caixa = reg
                    elif reg_12_unidade is not None:
                        # @todo Ver de onde obter o preco e a quantidade da caixa
                        linea_atacado_12 = nova_linea_atacado_12(quantidades_atacado, reg_12_unidade, reg_12_caixa, reg_10_caixa)
                        empoatac_file.write(linea_atacado_12)
                        reg_10_caixa = None
                        reg_12_unidade = None
                        reg_12_caixa = None
                        tipo_reg_anterior = None

                    empoatac_file.write(line)

            except QuantidadeAtacadoNaoDefinida:
                empoatac_file.write(line)

            tipo_reg_anterior = tipo_reg



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
