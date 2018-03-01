import urllib2
from lxml import etree

from selenium_utils import get_headed_driver, get_headless_driver
from iterator import _gen_tree


class Tree:
    def __init__(self, url=None):
        if url is None:
            pass
        else:
            self.get_url(url)

    def get_url(self, url):
        request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib2.urlopen(request)
        htmlparser = etree.HTMLParser()
        self.tree = etree.parse(response, htmlparser)

    def xpath(self, xpath):
        return self.tree.xpath(xpath)


class Engine:
    def __init__(self, type='selenium', **kwargs):
        if type is 'lxml':
            self.core = Tree()
        else:
            if kwargs['headed']:
                self.core = get_headed_driver()
            if kwargs['headless']:
                self.core = get_headless_driver()