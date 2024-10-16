import os, sys
from pathlib import Path
BASE_DIR = str(Path(os.path.dirname(__file__)).parent.parent)
BACK_DIR = BASE_DIR + '/backend'
DATA_DIR = BACK_DIR + '/data'
LOG_DIR = BACK_DIR + '/logs'
# Configuração básica do logging
import logging 
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=f'{LOG_DIR}/app.log',  # Nome do arquivo de log
                    filemode='a')  # 'w' sobrescreve o arquivo a cada execução, 'a' anexa ao arquivo

