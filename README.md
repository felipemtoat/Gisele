# Gisele

Este projeto é um estudo para automatizar a separação de históricos escolares escaneados em lote. O objetivo foi dividir um PDF contendo vários históricos em arquivos individuais, baseando-se na contagem de páginas (identificada pelo padrão `Pág. x de y`) e salvando cada histórico com o nome do aluno extraído do próprio scan.

## Funcionamento

- Utiliza OCR para extrair o texto das páginas escaneadas.
- Identifica o início e fim de cada histórico pela paginação.
- Extrai o nome do aluno do texto para nomear o arquivo PDF gerado.
- Cada histórico deveria ter no máximo 3 páginas.

## Limitações encontradas

- O resultado do OCR não foi satisfatório, dificultando a extração confiável do texto.
- Muitos históricos estavam sendo salvos com mais de 3 páginas devido a falhas na leitura.
- Foi implementado um verificador para refazer a leitura caso o número de páginas do histórico estivesse incorreto.