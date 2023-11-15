import argparse
import urllib.request
import pyyaml

parser = argparse.ArgumentParser()
parser.add_argument('--depth', type=int)
parser.add_argument('--ignore-regex', type=str)
parser.add_argument('url', type=str)





def make_dict(url):
    temp = [{"level":i, "links":[]} for i in range(depth+1)]
    output = {"root":url, "web":temp}
    output[web][0][0]["links"] = [url]


def get_html(url):
    web_url = urllib.request.urlopen(url)
    data = weburl.read()
    return data

def scan_urls(html_code):
    i = 0
    last_index = 0
    urls_lst = []
    while i < len(html_code):
        current_index = html_code.find('href="', last_index) #index of h
        if current_index != -1:
            j = current_index+6
            lst = [html_code[j]]
            while html_code[j] != '"':
                lst.append(html_code[j])
                j += 1
            link = "".join(lst)
            if not link in urls_lst:
                urls_lst.append(link)
    return urls_lst


def get_all_urls(depth, depth_curr, url):
    dict = {}
    dict[depth-depth_curr] = scan_urls(url)
    new_lst = [] #not done!
    for link in dict[depth]:
        new_lst.append(get_all_urls(depth, depth_curr+1, link))









