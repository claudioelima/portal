from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Response
from app.scraping.scrap import fetch_page, parse_html, extract_data, parse_detail_page
from app.scraping.csv import save_to_csv_in_memory

routes = Blueprint('routes', __name__)

@routes.route("/")
def index():
    data = session.get('data', [])
    return render_template("index.html", data=data)

@routes.route("/scrape", methods=["POST"])
def scrape():
    job_type = request.form.get("job_type")
    max_pages = int(request.form.get("max_pages", 1))
    city = request.form.get("city")
    is_internship = request.form.get("is_internship")

    if not job_type or not city:
        flash("Por favor, preencha todos os campos.")
        return redirect(url_for('routes.index'))

    job_type = job_type.replace(" ", "-")
    city = city.replace(" ", "-") + "-sp"

    base_url = f'https://www.bne.com.br/vagas-de-emprego/'
    query_params = f'?Page='
    additional_params = f'&CityName={city}&Function={job_type}'

    if is_internship:
        additional_params += '&LinkType=Estágio'

    all_data = []

    for page in range(1, max_pages + 1):
        url = base_url + query_params + str(page) + additional_params
        print(f"Acessando: {url}")
        html = fetch_page(url)
        if not html:
            continue
        soup = parse_html(html)
        job_list = extract_data(soup)

        for job in job_list:
            detail_page_html = fetch_page(job['Continuar lendo'])
            if detail_page_html:
                details = parse_detail_page(detail_page_html)
                job.update(details)

        all_data.extend(job_list)

    if all_data:
        session['data'] = all_data[:100] 
    else:
        session['data'] = []

    return redirect(url_for('routes.index'))

@routes.route("/download")
def download():
    data = session.get('data', [])
    if data:
        csv_data = save_to_csv_in_memory(data)
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment;filename=vagas.csv'}
        )
    else:
        flash("Nenhuma vaga encontrada para download.")
        return redirect(url_for('routes.index'))