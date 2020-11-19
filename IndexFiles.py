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

import argparse
import os
import codecs

def main():
    if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, default=None, help='Path to the files')
    parser.add_argument('--index', required=True, default=None, help='Index for the files')

    args = parser.parse_args()

    # path to folder with documents to be indexed
    PATH_NAME = args.path
    # index name
    INDEX_NAME = args.index

    lfiles = generate_files_list(PATH_NAME)
    print('Indexing %d files'%len(lfiles))
    print('Reading files ...')
    
    # Reads all the documents in a directory tree and generates an index operation for each
    ldocs = []
    for f in lfiles:
        ftxt = codecs.open(f, "r", encoding='iso-8859-1')

        text = ''
        for line in ftxt:
            text += line
        # Insert operation for a document with fields 'path' and 'text'
        ldocs.append({'_op_type': 'index', '_index': INDEX_NAME, 'path': f, 'text': text})

    # Working with ElasticSearch
    client = Elasticsearch()

    # Drop index if it exists
    if client.indices.exists(INDEX_NAME):
        client.indices.delete(INDEX_NAME)
    # Create index and ignore 400 cause by IndexAlreadyExistsException when creating an index.
    client.indices.create(index=INDEX_NAME, ignore=400)

    # Bulk execution of elasticsearch operations (faster than executing all one by one)
    print('Indexing ...')
    bulk(client, ldocs)
    