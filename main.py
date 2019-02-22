import requests
import sys
import os
import json
import fileIO
import bs4
import re

def tokenize(y) -> list:
    token = []
    for text in y:
        text = text.rstrip()
        p = re.compile("[a-z]+") #pattern for token
        l = p.findall(text.lower()) #make a list of words that fit pattern
        token.extend(l)
    return token
    
    
def search(index, searchterm) -> list:
    searchresult = index[searchterm]
    print("Number of URLs for '", searchterm, "':", len(searchresult))
    return searchresult

    
def create_index() -> (dict, int):
    rootdir = 'webpages\\WEBPAGES_RAW'
    result = dict()
    num_doc = 0

    with open('bookkeeping.json', 'r') as f:
            j_dict = json.load(f)

    for k, v in j_dict.items():

            num_doc += 1
            y = []
            
            fol, fil = k.split('/')
            
            try:
                    file = open(rootdir + "\\" + fol + "\\" + fil, 'r', encoding = 'utf-8')

                    soup = bs4.BeautifulSoup(file, 'lxml')
                    soup.prettify()
                    a_txt = soup.find_all('p')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in a_txt])

                    b_txt = soup.find_all('a')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                    b_txt = soup.find_all('b')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                    b_txt = soup.find_all('h1')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                    b_txt = soup.find_all('h2')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])


                    b_txt = soup.find_all('h3')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])

                    b_txt = soup.find_all('body')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])
                    
                    b_txt = soup.find_all('title')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])
                    
                    b_txt = soup.find_all('strong')
                    y.extend([re.sub(r'<.+?>',r'',str(a)) for a in b_txt])
                    
                    
            except:
                    with open(rootdir + "\\" + fol + "\\" + fil, 'r', encoding = 'utf-8') as d:
                            file_str = d.read().replace('\n', '')
                    #print(file_str)
                    y.append(file_str)
                    
            finally:
                    l = tokenize(y)
                    print(str(fol)+'/'+ str(fil))

                    for i in l:
                            freq = l.count(i)

                            if i not in result:
                                    result[i] = []
                            if (fol, fil, freq) not in result[i]:
                                result[i].append((fol,fil, freq))
            
    return (result, num_doc)

    
if __name__ == '__main__':
        index = None
        num_doc = None
        
        if fileIO.index_file_exists():
            print('Reading index from file...')
            index = fileIO.read_index_from_file()
            num_doc = fileIO.read_num_doc_from_file()
        else:
            print('Creating index...')
            index, num_doc = create_index()
            fileIO.write_index_to_file(index)
            fileIO.write_num_doc_to_file(num_doc)
        
        
        print('Number of documents:', num_doc)
        num_uniq = len(index)
        print('Number of uniques:', num_uniq)
        print('Size of index on file:', os.path.getsize("final.txt"), 'bytes')

        searchresult = search(index, 'slide')
            
        # info_list = index["mondego"]
        # print("URLs for word: mondego")
        # print(len(info_list))
        # for i in info_list:
            # print(j_dict[str(i[0]) + '/' + str(i[1])])
