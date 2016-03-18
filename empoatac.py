#!/usr/bin/python
#encoding=utf8


class QuantidadeAtacadoNaoDefinida(Exception):
    pass

def get_quantidades_atacado(quan_filename)

    quantidades_atacado = {}

    with open(quan_filename, 'r') as quan_file:
        for line in f:
            reg = line..strip().split('\t').strip()
            for i in range(len(reg)):
                reg[i] = reg[i].strip()
            # @todo Verificar si tem loja
            loja = reg[LOJA]
            material = reg[MATERIAL]
            quantidade = reg[QUANTIDADE]
            if loja not in quantidades_atacado:
                quantidades_atacado[loja] = {material: quantidade}
            else:
                quantidades_atacado[loja][material] = quantidade

    return quantidades_atacado


def reg_to_linea_atacado(quantidades_atacado, reg):
    tipo_reg = reg[TIPO_REG]
    loja = reg[LOJA]
    plu = reg[PLU]
    material = plu[:-2]
    um = plu[-2:]

    try:
        quantidade_atacado = quantidades_atacado[loja][material] 
    except KeyError:
        raise QuantidadeAtacadoNaoDefinida()

    reg[QUANTIDADE_ATACADO] = quantidade_atacado
    
    return '|'.join(reg)


def nova_linea_atacado_12(quantidades_atacado, reg_anterior, preco_caixa, quantidade_caixa):
    
    

def convert_emporium_to_emporium_atacado(quantidades_atacado, empo_filename, extencao_novo_arquivo):
    
    empoatac_filename = u'%s.%s' % (empoatac_filename, extencao_novo_arquivo)

    with open(empo_filename, 'r') as empo_file, open(empoatac_filename, 'w') as empoatac_file:
        for line in empo_file:
            reg = line.split('|')
            tipo_reg = reg[TIPO_REG]

            try:
                if tipo_reg in ['11', '12']:
                    linea_atacado = reg_to_linea_atacado(quantidades_atacado, reg)
                    empoatac_file.write(linea_atacado)
                else:
                    if tipo_reg_anterior == '12':
                        # @todo Ver de onde obter o preco e a quantidade da caixa
                        linea_atacado_12 = nova_linea_atacado_12(quantidades_atacado, reg_anterior, preco_caixa, quantidade_caixa)
                        empoatac_file.write(linea_atacado_12)
                    empoatac_file.write(line)

            except QuantidadeAtacadoNaoDefinida:
                empoatac_file.write(line)
                
            tipo_reg_anterior = tipo_reg
            reg_anterior = reg



def empoatac(quan_filename, empo_filenames):

    quantidades_atacado = get_quantidades_atacado(quan_filename)

    for empo_filename in empo_filenames:
        convert_emporium_to_emporium_atacado(
            quantidades_atacado,
            empo_filename,
            'new'
            )
    
