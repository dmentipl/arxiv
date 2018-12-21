'''
arxiv.py
Daniel Mentiplay, 2018.
'''

import urllib.request

class Arxiv:
    '''
    Contains a list of entries from my daily arXiv email.
    '''

    def __init__(self):

        self.date = None
        self.entries = None
        self.categories = None

        self._read_data_from_file()
        self._get_categories()

    def _read_data_from_file(self):

        entries = list()

        filename = 'original_msg.txt'

        in_entries = False
        in_abstract = False
        in_title = False
        in_authors = False
        in_comments = False

        keys = ['label', 'date', 'title', 'comments', 'categories', 'abstract',
                'journal-ref', 'doi']

        with open(filename, 'r') as file:

            prevLine = ''

            for line in file:
                line = line.rstrip('\n')

                if line == 78*'-':
                    in_entries = True
                    continue

                if not in_entries:
                    continue

                if ' received from' in line:
                    words = line.split('  ')
                    self.date = words[3]

                if '%%--%%' in line:
                    break

                if 'arXiv:' in line:
                    entry = {key: None for key in keys}
                    entry['label'] = line[:16]
                    continue

                if 'Date:' in line:
                    words = line.split(' ')
                    entry['date'] = words[2] + ' ' + words[3] + ' ' + words[4]
                    continue

                if 'Title:' in line:
                    in_title = True
                    entry['title'] = line[7:]
                    continue

                if in_title:
                    if line[0:2] == '  ':
                        entry['title'] += line[1:]
                        continue
                    else:
                        in_title = False

                if 'Authors:' in line:
                    in_authors = True
                    authors_line = line[9:]
                    continue

                if in_authors:
                    if line[0:2] == '  ':
                        authors_line += line[1:]
                        continue
                    else:
                        entry['authors'] = authors_line.split(', ')
                        in_authors = False

                if 'Categories:' in line:
                    entry['categories'] = line[12:].split(' ')
                    continue

                if 'Comments:' in line:
                    in_comments = True
                    entry['comments'] = line[10:]
                    continue

                if in_comments:
                    if line[0:2] == '  ':
                        entry['comments'] = entry['comments'] + ' ' + line
                        continue
                    else:
                        in_comments = False

                if 'DOI:' in line:
                    entry['doi'] = line[5:]
                    continue

                if 'Journal-ref:' in line:
                    entry['journal-ref'] = line[13:]
                    continue

                if prevLine == r'\\' and line[0:2] == '  ':
                    in_abstract = True
                    entry['abstract'] = line[2:]
                    continue

                if in_abstract:
                    if line[0:2] != r'\\':
                        entry['abstract'] += ' ' + line
                        continue
                    else:
                        in_abstract = False
                        words = line.split(' ')
                        entry['url'] = words[2]
                        entries.append(entry)
                        continue

                prevLine = line

        self.entries = entries

    def _get_categories(self):
        '''Put all categories into a set'''

        categories = set()
        for entry in self.entries:
            for category in entry['categories']:
                categories.add(category)

        self.categories = categories

    def get_articles_from_category(self, category):
        '''Put all article labels with a particular category into a set'''

        if category not in self.categories:
            raise ValueError(f'{category} not in available categories')

        articles = set()
        for entry in self.entries:
            for category_ in entry['categories']:
                if category_ == category:
                    articles.add(entry['label'])

        return articles

    def get_url_from_label(self, label):
        '''Get url from article label'''

        url = None
        for entry in self.entries:
            if label == entry['label']:
                url = entry['url']

        if url is None:
            raise ValueError(f'{label} not found')
        else:
            return url

def pdf_url_from_article_url(url):
    '''Get arXiv pdf url from abstract url'''

    return url[:18] + 'pdf' + url[21:] + '.pdf'

def download_pdf_from_article_url(url):
    '''Download arXiv pdf'''

    url = pdf_url_from_article_url(url)

    filename = url.split("/")[-1]

    with urllib.request.urlopen(url) as response, open(filename, 'wb') as outfile:
        data = response.read()
        outfile.write(data)
