import os
import json


def read_index_from_file() -> dict:
    file = open('final.txt', 'r')
    index = eval(file.read())
    file.close()
    return index

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
    
    # info_list = result["irvine"]
    # print("URLs for word: irvine")
    # print(len(info_list))

    # for i in info_list:
        # print(j_dict[str(i[0]) + '/' + str(i[1])])
    

if __name__ == '__main__':
    print(read_index_from_file())
