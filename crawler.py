import argparse
import urllib.request
import yaml

#parser = argparse.ArgumentParser()
#parser.add_argument('--depth', type=int)
#parser.add_argument('--ignore-regex', type=str)
#parser.add_argument('url', type=str)



def make_dict(url, depth):
    temp = [{"level":i, "links":[]} for i in range(depth+1)]
    output = {"root":url, "web":temp}
    output["web"][0]["links"] = [url]
    return output

def get_html(url):
    web_url = urllib.request.urlopen(url)
    data = web_url.read()
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
        i += 1
    return urls_lst

def get_all_urls(depth, url):
    dictionary = make_dict(url, depth)
    for i in range(1, depth+2):
        lst = []
        for j in dictionary["web"][i-1]["links"]:
            lst += scan_urls(get_html(j))
        dictionary["web"][i]["links"] = lst
    return yaml.dump(dictionary)



print(get_all_urls(1, "https://en.wikipedia.org/wiki/Chess"))







