import os
import random
import shutil
import time

# Função para criar um nome de arquivo com padrão similar ao que você descreveu
def create_z_pattern_name(length):
    # Define um padrão alternado de 'Z' e '.' para o nome do arquivo
    pattern = ''.join(['Z' if i % 2 == 0 else '.' for i in range(length)])
    return pattern

# Função para sobrescrever um arquivo com um padrão específico
def overwrite_with_pattern(file_path, pattern, size):
    try:
        with open(file_path, 'rb+') as file:
            file_size = os.path.getsize(file_path)
            if size > file_size:
                size = file_size
            file.write(pattern * (size // len(pattern) + 1)[:size])
    except Exception as e:
        print(f"Erro ao sobrescrever com padrão {pattern}: {e}")

# Função para sobrescrever com múltiplos padrões
def secure_overwrite(file_path):
    file_size = os.path.getsize(file_path)
    patterns = [b'\x00', b'\xFF', bytes(random.getrandbits(8) for _ in range(600)), bytes([random.randint(0, 255) for _ in range(600)])]
    
    # Aumentar o número de sobrescrições para 15 para garantir que o arquivo seja efetivamente destruído
    for _ in range(15):  # Sobrescrever 15 vezes com diferentes padrões
        for pattern in patterns:
            overwrite_with_pattern(file_path, pattern, file_size)

# Função para mover e sobrescrever arquivos de maneira segura
def secure_delete(path, script_path):
    if not os.path.exists(path):
        print(f"O caminho especificado não existe: {path}")
        return

    temp_dir = os.path.join(os.path.dirname(path), 'temp_delete')
    os.makedirs(temp_dir, exist_ok=True)

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                if file_path == script_path:
                    print(f"O próprio script não será excluído: {file_path}")
                    continue
                try:
                    # Renomeando o arquivo com um padrão de 'Z's
                    new_file_name = create_z_pattern_name(len(name))
                    new_file_path = os.path.join(temp_dir, new_file_name)
                    shutil.move(file_path, new_file_path)
                    
                    # Sobrescrevendo o arquivo com múltiplos padrões
                    secure_overwrite(new_file_path)
                    
                    # Apagar o arquivo após sobrescrever
                    os.remove(new_file_path)
                    print(f"Arquivo excluído: {new_file_path}")
                except Exception as e:
                    print(f"Erro ao excluir o arquivo {file_path}: {e}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                    print(f"Pasta excluída: {dir_path}")
                except Exception as e:
                    print(f"Erro ao excluir a pasta {dir_path}: {e}")
        attempts = 3
        for attempt in range(attempts):
            try:
                os.rmdir(path)
                print(f"Pasta excluída: {path}")
                break
            except Exception as e:
                print(f"Erro ao excluir a pasta {path} (tentativa {attempt + 1} de {attempts}): {e}")
                time.sleep(1)
        try:
            os.rmdir(temp_dir)
        except Exception as e:
            print(f"Erro ao remover diretório temporário: {e}")
    elif os.path.isfile(path):
        if path == script_path:
            print(f"O próprio script não será excluído: {path}")
            return
        try:
            # Renomeando o arquivo com um padrão de 'Z's
            new_file_name = create_z_pattern_name(len(os.path.basename(path)))
            new_file_path = os.path.join(temp_dir, new_file_name)
            shutil.move(path, new_file_path)
            
            # Sobrescrevendo o arquivo com múltiplos padrões
            secure_overwrite(new_file_path)
            
            # Apagar o arquivo após sobrescrever
            os.remove(new_file_path)
            print(f"Arquivo excluído: {new_file_path}")
        except Exception as e:
            print(f"Erro ao excluir o arquivo {path}: {e}")

# Resto do script permanece o mesmo
current_directory = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.abspath(__file__)

print(f"Iniciando exclusão no diretório: {current_directory}")

secure_delete(current_directory, script_path)

print("Exclusão completa.")
input("Pressione Enter para sair...")
