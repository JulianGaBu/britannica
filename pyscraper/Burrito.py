import urllib2
from lxml import etree

from selenium_utils import get_headed_driver, get_headless_driver
from iterator import _gen_tree

from contextlib import contextmanager


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



class Seleniumable:
    def __init__(self, driver):
        self.driver = driver

class Selectable(Seleniumable):
    def __init__(self, selector, driver):
        Seleniumable.__init__(self, driver)
        self.selector = selector

    def __new__(cls, *args, **kwargs):
        pass


class XPATHable(Selectable):
    def __init__(self, xpath, driver):
        Selectable.__init__(self, xpath, driver)

    def __new__(cls, *args, **kwargs):
        return cls.driver.find_elements_by_xpath(cls.selector)

    @property
    def if_exists(self):
        xpath = self.selector
        driver = self.driver
        if len(driver.find_elements_by_xpath(xpath)) < 1:
            return ''
        text = driver.find_element_by_xpath(xpath) if 'text' in xpath else driver.find_element_by_xpath(xpath).text
        return text.strip() if text else ''


class Byable(Seleniumable):

    def xpath(self, xpath):
        return XPATHable(xpath, self.driver)

class Findable(Seleniumable):

    @property
    def by(self):
        return Byable(self.driver)

    @property
    def frame(self):
        self.driver

        return

class Burrito:
    def __init__(self, headless=False, no_sandbox=False):
        self.driver = get_headless_driver(no_sandbox=no_sandbox) if headless else get_headed_driver()

    def __enter__(self):
        self.driver = get_headless_driver(no_sandbox=no_sandbox) if headless else get_headed_driver()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def get(self, url):
        self.driver.get(url)

    def visit(self, url):
        self.driver.get(url)

    @property
    def find(self):
        return Findable(self.driver)

class Burritree:
    def __init__(self, url):
        self.tree = _gen_tree(url)

    def get(self, url):
        self.tree = _gen_tree(url)

    def get_tree(self):
        return self.tree

    def get_xpath_if_exists(self, xpath):
        if len(self.tree.xpath(xpath)) < 1:
            return ''
        text = self.tree.xpath(xpath)[0] if 'text' in xpath else self.tree.xpath(xpath)[0].text
        return text.strip() if text else ''

@contextmanager
class Kekrrito:
    def __init__(self, string):
        pass






burrito = Burrito()
burrito.get('https://www.mass.gov/locations/brockton-district-court')
test = burrito.find.by.xpath('//*[@id="accordion1"]/div/h2/span').if_exists
print test
print 'h'



