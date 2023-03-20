#!/bin/bash
echo "Updating PlexAniSync"
wget https://github.com/RickDB/PlexAniSync/archive/master.zip &&\
unzip master.zip &&\
rm master.zip &&\
cp -f /PlexAniSync-master/*.py /plexanisync
cp -rf /PlexAniSync-master/plexanisync /plexanisync/plexanisync
cp -f /PlexAniSync-master/requirements.txt /plexanisync/requirements.txt
rm -rf /PlexAniSync-master
cd /plexanisync &&\
python -m pip install -r requirements.txt &&\
cd ..
echo "Update completed successfully"