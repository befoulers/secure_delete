# Exclusão Segura de Arquivos e Pastas

Este script em Python realiza a exclusão **irreversível** de arquivos e pastas, sobrescrevendo o conteúdo com dados aleatórios antes de apagá-los.

## Passo a Passo

1. **Clone o repositório** para sua máquina local:
    ```bash
    git clone https://github.com/befoulers/secure_delete.git
    ```

2. **Navegue até o diretório** onde o script está localizado:
    ```bash
    cd secure_delete
    ```

3. **Certifique-se de ter o Python instalado**. Caso não tenha, baixe o Python [aqui](https://www.python.org/downloads/).

4. **Execute o script**:
    ```bash
    python secure_delete.py
    ```

   O script vai excluir todos os arquivos e subpastas dentro da pasta onde ele está, **sem excluir o próprio script**.

## Importante

- **Irreversível**: Os arquivos e pastas excluídos não podem ser recuperados.
- **O próprio script não será excluído**.