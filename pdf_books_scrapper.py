from bs4 import BeautifulSoup
import requests
import json

def table_dict(table):
    json={}
    rows=table.find_all('tr')[1:]
    for row in rows:
        rjson={}
        tds=row.find_all('td')

        rjson['Title']=tds[1].text.strip()
        rjson['URL']=f"https://upagripardarshi.gov.in/{tds[1].a['href'][3:]}"

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

print(scrapping())
with open("pdf_data.json", "w") as outfile: 
    json.dump(scrapping(), outfile)