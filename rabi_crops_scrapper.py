from bs4 import BeautifulSoup
import requests
import json

def table_parser(table):
    api_key='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'
    openAI_url="https://api.openai.com/v1/chat/completions"

    header={
    'Authorization':'Bearer '+api_key,
    'Content-Type':'application/json'
    }

    payload={
    'model':'gpt-3.5-turbo',
    'messages':[
        {"role": "user", "content": f"I will give you the HTML code of the table. You have to give content of the table in JSON form. Table HTML code: {str(table)}. Give only JSON in single line"},
    ]
    }


    response = requests.post(openAI_url, headers=header, json=payload)
    if response.status_code == 200:
        table_json=response.json()['choices'][0]['message']['content'].strip()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        table_json='error parsing table'

    return table_json

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

'''def scrapping(home_page):
    pages=get_pages(home_page)
    size_pages=len(pages)
    page_data={}
    current_heading=''
    flag=0
    for i,page in enumerate(pages):
        print(f'{i+1}/{len(pages)} pages fetched',end='\r')
        response = requests.get(f'https://upagripardarshi.gov.in/StaticPages/{page}')
        crop_soup = BeautifulSoup(response.text, 'html.parser')
        content=crop_soup.find('div','col-md-9')
        tags=content.find_all(['h4','p','li'])
        if size_pages>1:
            tags=tags[:-(size_pages+2)] #to eliminate pagination list at the end
        for i,tag in enumerate(tags[1:]):
            if tag.name == 'h4' or (tag.name == 'p' and tag.find('strong')):
                current_heading = tag.text
                page_data[current_heading] = []
                flag=1
            else:
                flag=0
                if current_heading=='':
                    current_heading='General'
                    page_data[current_heading] = []
                page_data[current_heading].append(tag.text)
    return page_data'''

def scrapping(home_page):
    pages = get_pages(home_page)
    size_pages = len(pages)
    page_data = {}
    current_main_heading = ''
    current_subheading = ''
    
    for i, page in enumerate(pages[0:1]):
        print(f'{i+1}/{len(pages)} pages fetched', end='\r')
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
            if tag.name == 'h4':
                current_main_heading = tag.text.strip()
                current_subheading = ''  # Reset subheading when a new main heading is found
                if current_main_heading not in page_data:
                    page_data[current_main_heading] = {}
            elif tag.name == 'p' and tag.find('strong'):
                current_subheading = tag.text.strip()
                if current_main_heading not in page_data:
                    page_data[current_main_heading] = {}
                if current_subheading not in page_data[current_main_heading]:
                    page_data[current_main_heading][current_subheading] = []
            elif current_main_heading and current_subheading:
                # Only add content if both main heading and subheading are available
                if tag.name=='table':
                    data=table_parser(tag)
                else:
                    data=tag.text.strip()
                page_data[current_main_heading][current_subheading].append(data)

                
            else:
                if current_main_heading and not current_subheading:
                    current_subheading='General'
                    page_data[current_main_heading][current_subheading]=[]
                if not current_main_heading and not current_subheading:
                    current_main_heading='General'
                    current_subheading='General'
                    page_data[current_main_heading]={}
                    page_data[current_main_heading][current_subheading]=[]
                if tag.name=='table':
                    data=table_parser(tag)
                else:
                    data=tag.text.strip()
                page_data[current_main_heading][current_subheading].append(data)
                
                

    return page_data

rabi_crops=extract_rabi_links()
crop_json_data={}
for crop in rabi_crops:
    crop_data={}
    print(crop)
    url=f'https://upagripardarshi.gov.in/StaticPages/{crop[2]}'
    crop_data['S.No.']=crop[0]
    crop_data['Name']=crop[1]
    crop_data['URL']=url
    crop_data['Content']=scrapping(crop[2])
    print(crop_data['Content'])
    crop_json_data[crop[1]]=crop_data

print('****************')
print(crop_json_data)
print(len(crop_json_data))  
with open("crop_data.json", "w") as outfile: 
    json.dump(crop_json_data, outfile)