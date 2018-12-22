'''
download_astro_ph_EP_pdfs.py
Daniel Mentiplay, 2018.

This script downloads all the pdfs in astro-ph.EP for the arXiv email in the
current directory. Assumes the arXiv email is called 'original_msg.txt'.
'''

from arxiv.arxiv import Arxiv, download_pdf_from_article_url

arxiv = Arxiv()

for article in arxiv.get_articles_from_category('astro-ph.EP'):
    url = arxiv.get_url_from_label(article)
    download_pdf_from_article_url(url)
