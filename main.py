import requests
import sys
import os
import json
import readfile
import bs4
import re

def printResult(result):
        for k, v in result.items():
                print(k, v)
                
def printList(node):
        pass

if __name__ == '__main__':
        rootdir = 'testwebpages'
        result = {}
        y = []
        z = []
        for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                        path = os.path.join(subdir, file)
                        filename = path.split('\\')[-1]
                        file = readfile.read_file(path)
                        soup = bs4.BeautifulSoup(file, 'html.parser')

                       
                        a_txt = soup.find_all('p')
                        y.extend([re.sub(r'<.+?>',r'',str(a)) for a in a_txt])

                        b_txt = soup.find_all('td')
                        z.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])
                        #print(y)
                        #print(z)
        c = y + z
        for i in c:
                new_str = re.sub('[^a-zA-Z0-9]', ' ',i.lower())
                new_str = new_str.split()
                for x in new_str:
                        if x in result:
                                result[x] += 1
                        else:
                                result[x] = 1
        print(result)

        
                        
