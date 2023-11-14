from bs4 import BeautifulSoup
import requests

def get_pages(crop):
    response = requests.get(f'https://upagripardarshi.gov.in/StaticPages/{crop}')
    crop_soup = BeautifulSoup(response.text, 'html.parser')
    pages=[crop]
    paginated_links=crop_soup.find('div','col-md-12 col-sm-12 text_alain_r')
    if paginated_links:
        paginated_links=paginated_links.find_all(['li'])
    else:
        return pages
    num=['2','3','4','5','6','7','8']
    for link in paginated_links:
        if link.text.strip() in num:
            pages.append(link.a['href'])
    return pages

def extract_rabi_links():
    rabi_crops=[]
    url = 'https://upagripardarshi.gov.in/StaticPages/RabhiCrop.aspx'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    
    table = soup.find('table')
    rows=table.find_all('tr')

    for i,row in enumerate(rows):
        if i==0:
            continue
        tds=row.find_all('td')
        rabi_crops.append((tds[0].text.strip()[:-1],tds[1].text.strip(),tds[1].a['href']))
        rabi_crops.append((tds[3].text.strip()[:-1],tds[4].text.strip(),tds[4].a['href']))
    
    print('*********************************')
    print(len(rabi_crops),'links extracted successfuly')
    print('*********************************')

    return rabi_crops
