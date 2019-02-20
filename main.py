import requests
import sys
import os
import json
import readfile, database
import bs4
import re

def printResult(result):
        for k, v in result.items():
                print(k, v)
                
def printList(node):
        pass

if __name__ == '__main__':
        database.createDatabase()
        # rootdir = 'testwebpages'
        # result = {}
        # y = []
        
        # for subdir, dirs, files in os.walk(rootdir):
                
                # for file in files:
                        # try:
                                # path = os.path.join(subdir, file)
                                # filename = path.split('\\')[-1]
                                # file = readfile.read_file(path)
                                # soup = bs4.BeautifulSoup(file, 'html.parser')

                               
                                # a_txt = soup.find_all('p')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in a_txt])

                                # b_txt = soup.find_all('a')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                                # b_txt = soup.find_all('b')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                                # b_txt = soup.find_all('h1')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                                # b_txt = soup.find_all('h2')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                                # b_txt = soup.find_all('h3')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                                # b_txt = soup.find_all('body')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                                # b_txt = soup.find_all('title')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                                # b_txt = soup.find_all('strong')
                                # y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                                # #print(y)
                                # #print(z)
                        # except:
                                # continue

        # for i in y:
                # new_str = re.sub('[^a-zA-Z]', ' ',i.lower())
                # new_str = new_str.split()
                # for x in new_str:
                        # if x in result:
                                # result[x] += 1
                        # else:
                                # result[x] = 1
        # print(result)

        
                        
