import os
import json


def read_index_from_file() -> dict:
    file = open('final.txt', 'r')
    index = eval(file.read())
    file.close()
    return index
	
	
def read_num_doc_from_file() -> dict:
    file = open('num_doc.txt', 'r')
    num_doc = int(file.read())
    file.close()
    return num_doc

def write_result_to_file(num_uniq, size):
    nd = open("results.txt", "w")
    nd.write('Number of uniques: ' + str(num_uniq) + '\n')
    nd.write('Size of index on file: ' + str(size) + 'bytes')
    nd.close()

	
def write_index_to_file(result):
    final = open("final.txt", "w")
    final.write(str(result))
    final.close()
	
	
def write_num_to_file(num_doc):
    nd = open("num_doc.txt", "w")
    nd.write(str(num_doc))
    nd.close()
	
	
def index_file_exists():
    return os.path.isfile('final.txt')
    
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
