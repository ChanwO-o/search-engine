import os
import json


def generate_results():
    with open('bookkeeping.json', 'r') as j:
        j_dict = json.load(j)
    
    with open('final.txt') as f:
        result_dict = json.load(f)

    '''
    info_list = result["informatics"]
    print("URLs for word: informatics")
    print(len(info_list))

    for i in info_list:
        print(j_dict[str(i[0]) + '/' + str(i[1])])

    
    info_list = result["mondego"]
    print("URLs for word: mondego")
    print(len(info_list))

    for i in info_list:
        print(j_dict[str(i[0]) + '/' + str(i[1])])
    '''
    
    info_list = result["irvine"]
    print("URLs for word: irvine")
    print(len(info_list))

    for i in info_list:
        print(j_dict[str(i[0]) + '/' + str(i[1])])
    

if __name__ == '__main__':
    generate_results()
