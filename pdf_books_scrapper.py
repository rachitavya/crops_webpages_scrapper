from bs4 import BeautifulSoup
import requests
import json

def table_dict(table):
    json={}
    rows=table.find_all('tr')[1:]
    for row in rows:
        rjson={}
        tds=row.find_all('td')

        title=tds[1].text.strip()
        rjson['Title']=title

        url=f"https://upagripardarshi.gov.in/{tds[1].a['href'][3:]}"
        rjson['URL']=url
        print(f'downloading{title}.pdf')
        download_pdf(url,f'output/books_pdf/{title}.pdf')

        type_str=tds[2].text.strip()
        type_split=type_str.split('|')

        rjson['File Type']=type_split[0]
        rjson['Size']=type_split[1][7:]
        rjson['Language']=type_split[2][7:]
        rjson['Date and Time']=tds[3].text.strip()

        json[tds[0].text.strip()]=rjson
        
    return json

def scrapping():
    response = requests.get(f'https://upagripardarshi.gov.in/StaticPages/IllustratedTechnicalBook.aspx')
    soup = BeautifulSoup(response.text, 'html.parser')
    h4_tags=soup.find_all('h4')
    tables=soup.find_all('table')
    res={}
    for tag,table in zip(h4_tags,tables):
        res[tag.text.strip()]=table_dict(table)
    
    return res

def download_pdf(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        with open(save_path, 'wb') as pdf_file:
            pdf_file.write(response.content)

        print(f"PDF downloaded successfully and saved to: {save_path}")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")

    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")

    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")

    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")


pdf_log=scrapping()
with open("output/books_pdf/pdf_log.json", "w") as outfile: 
    json.dump(pdf_log, outfile)