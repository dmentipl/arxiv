'''
download_astro_ph_EP_pdfs.py
Daniel Mentiplay, 2018.

Example script using arxiv python module.
'''

from arxiv import Arxiv, download_pdf_from_article_url

arxiv = Arxiv()

for article in arxiv.get_articles_from_category('astro-ph.EP'):
    url = arxiv.get_url_from_label(article)
    download_pdf_from_article_url(url)