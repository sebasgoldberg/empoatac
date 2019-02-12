Script de Adaptação de Arquivo de Preços entre Integrador e Emporium
--------------------------------------------------------------------

Execução
--------

    $ ./empoatac.py <arquivo_configuração_quantidades_atacado> [--BASE_NO_11] [<arquivo_preços>, ...]

Depois da execução, os arquivos de preço passados como argumento, terão as informações adicionais da modalidade quantidade de atacado.


Execução dos testes
-------------------

É recomendavel a execução dos testes para verificar o correto funcionamento do script:

    $ ./test.py

