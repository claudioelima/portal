import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_data(soup):
    job_list = []
    job_sections = soup.find_all('div', class_='job__header is-list')
    
    if not job_sections:
        print("Nenhuma seção de vaga encontrada.")
    
    for section in job_sections:
        job_data = {}
        
        title_element = section.find('div', class_='job__title')
        if title_element:
            title = title_element.find('a').text.strip()
            job_data['Título da Vaga'] = title
            job_data['Continuar lendo'] = 'https://www.bne.com.br' + title_element.find('a')['href']
        else:
            print("Nenhum título de vaga encontrado.")

        details = section.find_all('h3', class_='job__detail')
        if not details:
            print("Nenhum detalhe da vaga encontrado.")
        
        for detail in details:
            strong_tag = detail.find('strong')
            if strong_tag:
                key = strong_tag.text.strip(': ')
                value = detail.get_text(separator=' ', strip=True).replace(key + ': ', '')
                job_data[key] = value
            else:
                print("Tag <strong> não encontrada dentro do <h3>")
        
        job_list.append(job_data)
    
    return job_list

def parse_detail_page(html):

    soup = BeautifulSoup(html, 'html.parser')
    details = {}

    desc_geral = soup.find('summary', string='Descrição Geral')
    if desc_geral:
        details['Descrição Geral'] = desc_geral.find_next('pre').text.strip()
        
    requisitos = soup.find('summary', string='Requisitos')
    if requisitos:
        details['Requisitos'] = requisitos.find_next('pre').text.strip()

    atribuicoes = soup.find('summary', string='Atribuições')
    if atribuicoes:
        details['Atribuições'] = atribuicoes.find_next('pre').text.strip()

    tipo_vinculo = soup.find('summary', string='Tipo de Vínculo')
    if tipo_vinculo:
        details['Tipo de Vínculo'] = tipo_vinculo.find_next('pre').text.strip()
        
    beneficios = soup.find('summary', string='Benefícios')
    if beneficios:
        details['Benefícios'] = beneficios.find_next('pre').text.strip()
        
    cursos = soup.find('summary', string='Cursos')
    if cursos:
        details['Cursos'] = cursos.find_next('pre').text.strip()

    return details