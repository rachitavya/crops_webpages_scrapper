# Illustrated Technical Books PDF scrapper and downloader
1. Download the dependencies:
`pip install beautifulsoup4 requests`
2. Run pdf_books_scrapper.py file and the downloading will start
`python3 pdf_books_scrapper`
3. Output PDFs will be stored in `output/books_pdf/` folder.


# crops_webpages_pdf_scrapper
This is an under development scrapper repository where I am using python to scrap information from this [link](https://upagripardarshi.gov.in/StaticPages/RabhiCrop.aspx).

### Steps to run the scrapper:

#### For PDF Output
1. Open terminal and run this command to install all the required dependencies:
`pip install -r requirements.txt`
2. Run main.py
`python3 main.py`
3. Check the output pdf files for every crop in `output/rabi_crops_pdf` folder

#### For JSON Output
2. Put your OpenAI API key in a .env file
3. Run rabi_crops_scrapper.py
`python3 python main.py`
4. Check the output pdf files for every crop in `output/rabi_crops_json` folder
