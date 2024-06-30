import csv
import io
from unidecode import unidecode

def normalize_data(data):
    return [{k: unidecode(v) for k, v in entry.items()} for entry in data]

def save_to_csv_in_memory(data):
    if data and isinstance(data, list):
        data = normalize_data(data)  
        keys = ['Título da Vaga', 'Cargo/Função', 'Localização', 'Salário', 'Empresa', 'Descrição Geral', 'Atribuições', 'Tipo de Vínculo', 'Benefícios', 'Requisitos', 'Cursos', 'Continuar lendo']
        output = io.StringIO()
        dict_writer = csv.DictWriter(output, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
        return output.getvalue().encode('utf-8')
    return None
