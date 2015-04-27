#!/bin/sh
scp run_hadoop_direct_index.sh run_hadoop_inverted_index.sh  r.shayahmetov@hadoop1srv10.corp.mail.ru:~/infosearch/
scp direct_index_mapper.py direct_index_reducer.py stop_words.txt simple9.py varbyte.py r.shayahmetov@hadoop1srv10.corp.mail.ru:~/infosearch/src_direct_index
scp dictionary_direct_index_all inverted_index_mapper.py inverted_index_reducer.py stop_words.txt simple9.py varbyte.py r.shayahmetov@hadoop1srv10.corp.mail.ru:~/infosearch/src_inverted_index
