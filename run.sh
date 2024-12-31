#!/bin/bash

# Atualiza o sistema e instala o Python e pip se necessário
echo "Atualizando o sistema e instalando dependências..."
sudo apt update && sudo apt install -y python3 python3-pip

# Verifica se o ambiente virtual já existe, se não, cria um
if [ ! -d "venv" ]; then
    echo "Criando o ambiente virtual..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
echo "Ativando o ambiente virtual..."
source venv/bin/activate

# Instala os pacotes listados no requirements.txt
echo "Instalando dependências do requirements.txt..."
pip install -r requisitos.txt

# Executa o projeto
echo "Iniciando o projeto..."
python3 main.py  # Substitua 'main.py' pelo nome do seu ficheiro principal

# Mantém o ambiente ativo após a execução (opcional)
echo "Ambiente virtual ativado. Use 'deactivate' para sair."
exec $SHELL
