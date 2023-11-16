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
    return str(data)

def scan_urls(html_code, src):
    last_index = 0
    urls_lst = []
    while last_index < len(html_code):
        current_index = html_code.find('href="', last_index) #index of h
        if current_index != -1:
            j = current_index + 6
            lst = []
            while html_code[j] != '"':
                lst.append(html_code[j])
                j += 1
            last_index = j + 1
            if lst[0] == '/' and lst[1] != '/':
                link = src + "".join(lst)
            elif lst[0] == '/' and lst[1] == '/':
                if 's' in src:
                    link = 'https:' + "".join(lst)
                else:
                    link = 'http:' + ''.join(lst)
            else:
                link = "".join(lst)
            if link not in urls_lst:
                urls_lst.append(link)
        else:
            last_index = len(html_code)
    return urls_lst



def get_all_urls(depth, url):
    dictionary = make_dict(url, depth)
    for i in range(1, depth+1):
        lst = []
        for j in dictionary["web"][i-1]["links"]:
            try:
                urllib.request.urlopen(j)
                lst += scan_urls(get_html(j), get_site_name(j))
            except:
                continue
        dictionary["web"][i]["links"] = lst
    return yaml.dump(dictionary)


def get_site_name(url):
    counter = 0
    index = 0
    while index < len(url):
        if url[index] == '/':
            counter += 1
        if counter == 3:
            return url[0:index]
        index += 1
    return url


#The input must be http / https site because of package limitations.
print(get_all_urls(1, 'https://he.wikipedia.org/wiki/%D7%9E%D7%A1%D7%98%D7%99%D7%A7'))







