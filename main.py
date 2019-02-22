import requests
import sys
import os
import json
import readfile
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

if __name__ == '__main__':
        
        rootdir = 'testwebpages'
        result = dict()
        num_doc = 0
        num_uniq = 0

        with open('bookkeeping.json', 'r') as f:
                j_dict = json.load(f)

        for k, v in j_dict.items():
                if int(k[0]) < 1:
            
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
                else:
                    break
                

                            
        final = open("final.txt", "w")
        final.write(str(result))
        final.close()
        
        print(num_doc)
        num_uniq = len(result)
        print(num_uniq)
        print(os.path.getsize("final.txt"))

    
        info_list = result["mondego"]
        print("URLs for word: mondego")
        print(len(info_list))
        for i in info_list:
            print(j_dict[str(i[0]) + '/' + str(i[1])])
