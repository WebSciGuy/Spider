from html.parser import HTMLParser
from urllib import parse
from domain import get_domain_name


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        base_url = get_domain_name(page_url)
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # when we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
