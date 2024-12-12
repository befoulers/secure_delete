import os
import random
import time

def overwrite_file(file_path):
    """Sobrescreve o conteúdo do arquivo com dados aleatórios."""
    if not os.path.isfile(file_path):
        print(f"Não é um arquivo: {file_path}")
        return

    # Obter o tamanho do arquivo
    file_size = os.path.getsize(file_path)
    
    try:
        with open(file_path, 'wb') as file:
            # Cria um buffer de dados aleatórios
            random_data = bytearray(random.getrandbits(8) for _ in range(file_size))
            file.write(random_data)
    except Exception as e:
        print(f"Erro ao sobrescrever o arquivo {file_path}: {e}")

def secure_delete(path, script_path):
    """Exclui arquivos e pastas de forma irreversível, sem excluir o próprio script."""
    if not os.path.exists(path):
        print(f"O caminho especificado não existe: {path}")
        return

    if os.path.isdir(path):
        # Se for uma pasta, exclua todos os arquivos e subpastas recursivamente
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                if file_path == script_path:
                    print(f"O próprio script não será excluído: {file_path}")
                    continue
                try:
                    overwrite_file(file_path)
                    os.remove(file_path)
                    print(f"Arquivo excluído: {file_path}")
                except Exception as e:
                    print(f"Erro ao excluir o arquivo {file_path}: {e}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                    print(f"Pasta excluída: {dir_path}")
                except Exception as e:
                    print(f"Erro ao excluir a pasta {dir_path}: {e}")
        # Tentar excluir a pasta com um atraso e várias tentativas
        attempts = 5
        for attempt in range(attempts):
            try:
                os.rmdir(path)
                print(f"Pasta excluída: {path}")
                break
            except Exception as e:
                print(f"Erro ao excluir a pasta {path} (tentativa {attempt + 1} de {attempts}): {e}")
                time.sleep(1)  # Aguarde um pouco antes de tentar novamente
    elif os.path.isfile(path):
        if path == script_path:
            print(f"O próprio script não será excluído: {path}")
            return
        try:
            overwrite_file(path)
            os.remove(path)
            print(f"Arquivo excluído: {path}")
        except Exception as e:
            print(f"Erro ao excluir o arquivo {path}: {e}")

# Pega o diretório atual onde o script está localizado
current_directory = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.abspath(__file__)

print(f"Iniciando exclusão no diretório: {current_directory}")

# Executa a exclusão segura no diretório atual e subpastas
secure_delete(current_directory, script_path)

print("Exclusão completa.")

# Mantém o terminal aberto após a execução
input("Pressione Enter para sair...")
