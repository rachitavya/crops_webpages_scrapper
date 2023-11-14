import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from utils import *

def scrapping(home_page):
    pages = get_pages(home_page)
    size_pages = len(pages)
    html_content=''
    
    for i, page in enumerate(pages):
        response = requests.get(f'https://upagripardarshi.gov.in/StaticPages/{page}')
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        crop_soup = BeautifulSoup(response.text, 'html.parser')
        content = crop_soup.find('div', 'col-md-9')
        tags = content.find_all(['h4', 'p', 'li','table'])
        
        if size_pages > 1:
            tags = tags[:-(size_pages + 2)]  # to eliminate pagination list at the end

        for tag in tags[1:]:
            html_content=f'{html_content}{tag}'

    print(f'{i+1}/{len(pages)} pages fetched', end='\r')
    return html_content
        

rabi_crops=extract_rabi_links()
print(len(rabi_crops))
html_content=''
for crop in rabi_crops:
    try:
        print(crop)
        url=f'https://upagripardarshi.gov.in/StaticPages/{crop[2]}'
        html_content=f'{html_content}{scrapping(crop[2])}'
        html_file=f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sample HTML to PDF</title>
    </head>
    <body>
        <h1>Hello, WeasyPrint!</h1>
        <p>This is a simple example HTML file.</p>
        {html_content}
    </body>
    </html>'''
        pdf_file = f"output/rabi_crops_pdf/[{crop[0]}]{crop[1]}.pdf"

        HTML(string=html_file).write_pdf(pdf_file)
    
    except:
        print('error in',crop)


