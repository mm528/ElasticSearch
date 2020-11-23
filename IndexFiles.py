# -*- coding: utf-8 -*-
"""
EPL660: Information Retrieval and Search Engines

ElasticSearch Lab

IndexFiles
**********

Indexes a set of files under the directory passed as a parameter (--path)
in the index name passed as a parameter (--index)

If the index exists it is dropped and created new

The documents are created with a 'path' and a 'text' fields

"""

from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import NotFoundError
import requests
import argparse
import os
import codecs
ldocs = []
client = Elasticsearch("http://localhost:9200")

def generate_files_list(path):
    """
    Generates a list of all the files inside a path (recursivelly)
    :param path:
    :return:
    """
    lfiles = []
    # generates the file names in a directory tree by walking the tree either top-down or bottom-up
    for lf in os.walk(path):
        print (path)
        # for every folder returns [root of each directory, sub-directories, files]
        if lf[2]:
            for f in lf[2]:
                lfiles.append(lf[0] + '/' + f)
    return lfiles





def main(path, indexname):
    resp = requests.get('http://localhost:9200/?pretty')
    if __name__ != '__main__':
        # path to folder with documents to be indexed
        PATH_NAME = path
        # index name
        INDEX_NAME = indexname
        print (PATH_NAME)
        lfiles = generate_files_list(PATH_NAME)
        print('Indexing %d files'%len(lfiles))
        print('Reading files ...')
        
        # Reads all the documents in a directory tree and generates an index operation for each
        
        for f in lfiles:
            ftxt = codecs.open(f, "r", encoding='iso-8859-1')

            text = ''
            for line in ftxt:
                text += line
            # Insert operation for a document with fields 'path' and 'text'
            ldocs.append({'_op_type': 'index', '_index': INDEX_NAME, 'path': f, 'text': text})
    
    # Working with ElasticSearch
   
    try:
        resp = requests.get('http://localhost:9200/?pretty')
        print(resp.content)
        client = Elasticsearch("http://localhost:9200")

        
        
            # index name 
        INDEX_NAME = indexname

        # Drop index if it exists
        if client.indices.exists(INDEX_NAME):
            client.indices.delete(INDEX_NAME)
        # Create index and ignore 400 cause by IndexAlreadyExistsException when creating an index.
        client.indices.create(index=INDEX_NAME, ignore=400)

        # Bulk execution of elasticsearch operations (faster than executing all one by one)
        print('Indexing ...')
        bulk(client, ldocs)

    except Exception:
        print('Elastic search is not running')
    
    