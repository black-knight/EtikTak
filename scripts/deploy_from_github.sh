#!/bin/bash

cd ~/download
wget https://nodeload.github.com/black-knight/EtikTak/zip/master
unzip master

cd EtikTak-master

sed -i 's/\.sqlite3/.mysql/g' EtikTakProject/settings.py
sed -i 's/database\.db/dnla_etiktak/g' EtikTakProject/settings.py
sed -i 's/''USER'': ''''/''USER'': ''dnla_etiktak''/g' EtikTakProject/settings.py
sed -i 's/''PASSWORD'': ''''/''PASSWORD'': ''REPLACE_ON_HOST''/g', EtikTakProject/settings.py

mv * ~/webapps/etiktak/

cd ~/download
rm master EtikTak-master

