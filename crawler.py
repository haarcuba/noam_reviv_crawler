'''
This is Raviv's and Noam's project :)
'''

import argparse
import urllib.request
import yaml
import re

#gets input from user
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--depth', type=int, default=2)
parser.add_argument('-ir', '--ignore_regex', type=str, default="^$") #compatible only with the string: "", there is no url like this!
parser.add_argument('url', type=str)
arguments = parser.parse_args()

depth = arguments.depth
regex = arguments.ignore_regex
url = arguments.url


def scan_urls_href(html_code, src):
    '''
    return a list of all the urls from a url (html_code)
    using attribute src
    '''
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
            #makes the links readable by the library
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


def scan_urls_src(html_code, src, new_lst):
    '''
    return a list of all the urls from a url (html_code)
    using attribute src
    '''
    last_index = 0
    url_lst = []
    while last_index < len(html_code):
        current_index = html_code.find('src="', last_index)
        if current_index != -1:
            j = current_index = 6
            lst = []
            while html_code[j] != '"':
                lst.append(html_code[j])
                j += 1
            last_index = j + 1
            #makes the links readable by the library
            if lst[0] == '/' and lst[1] != '/':
                link = src + "".join(lst)
            elif lst[0] == '/' and lst[1] == '/':
                if 's' in src:
                    link = 'https:' + "".join(lst)
                else:
                    link = 'http:' + "".join(lst)
            else:
                link = "".join(lst)
            if link not in urls_lst and link not in new_lst:
                urls_lst.append(link)
        else:
            last_index = len(html)
    return urls_lst


def get_all_urls(regex, depth, url):
    '''
    the main function
    defines the dictionary
    adds the urls
    converts to yaml
    '''
    temp = [{"level":i, "links":[]} for i in range(depth+1)]
    dictionary = {"root":url, "web":temp}
    dictionary["web"][0]["links"] = [url]

    for i in range(1, depth+1):
        lst = []
        for j in dictionary["web"][i-1]["links"]:
            #try so we dont get a 404/403 error
            try:
                if not re.search(regex, j):
                    data = str(urllib.request.urlopen(j).read())
                    src_site = get_site_name(j)
                    lst += scan_urls_href(data, src_site)
                    lst += scan_urls_src(data, src_site, lst)
            except:
                continue
        dictionary["web"][i]["links"] = lst

    return yaml.dump(dictionary)


def get_site_name(url):
    '''
    get the name of the parent site.
    example: https://en.wikipedia.org/wiki/Chess => https://en.wikipedia.org
    '''
    counter = 0
    index = 0
    while index < len(url):
        if url[index] == '/':
            counter += 1
        if counter == 3:
            return url[0:index]
        index += 1
    return url

#calls the main funtion and prints the yaml
#doesn't work for non http/https site because of library limitations
print(get_all_urls(regex, depth, url))

