from bs4 import BeautifulSoup
import re
import unittest

def is_true(tag):
    if tag.text[0] == "E" or tag.text[0] == "T" or tag.text[0] == "C":
        return True
    else:
        return False

def images(soup):
    imgs = 0
    for img in soup.find("div", id='bodyContent').find_all("img", width=re.compile(r"^")):
        if int(img["width"]) >= 200:
            imgs += 1
    return imgs

def headers_f(soup):
    head = [tag for tag in soup.find('div', id='bodyContent').find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    headers = []
    for tag in head:
        if is_true(tag):
            headers.append(tag)
        else:
            continue
    return len(headers)

def linkslen(soup):
    b = soup.find("div", {'id':'bodyContent'})
    tmp = soup.h1.string
    a = [link for link in b.find_all('a')]
    maxx = 0
    for link in a:
        max = 1
        while True:
            if isinstance(link.next_sibling, type(a[1])):
                if link.next_sibling.name == "a":
                    max+=1
                    link = link.next_sibling
                else:
                    break
            if isinstance(link.next_sibling, type(tmp)):
                link = link.next_sibling
                continue
            if isinstance(link.next_sibling, type(None)):
                break
            break
        if max > maxx:
            maxx = max
    return maxx


def lists(soup):
    sum = 0
    #########
    b = [ul for ul in soup.find("div", id='bodyContent').findAll("ul")]

    for ul in b:
        parents = [par.name for par in ul.parents]
        if "ul" not in parents and "ol" not in parents:
            sum+=1
        else:
            continue

    #########
    b = [ol for ol in soup.find("div", id='bodyContent').findAll("ol")]
    for ol in b:
        parents = [par.name for par in ol.parents]
        if "ul" not in parents and "ol" not in parents:
            sum+=1
        else:
            continue
    return sum

def parse(path_to_file):
    soup = BeautifulSoup(open(path_to_file, 'r', encoding="UTF-8").read(), features="lxml")
    return [images(soup), headers_f(soup), linkslen(soup), lists(soup)]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()




