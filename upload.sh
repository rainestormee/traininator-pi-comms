echo 'Uploading Server'
scp ./main/server.py ./main/pinio.py  rpi:/home/pi
echo 'Done'
echo 'Uploading Client'
scp ./main/client.py ./main/pinio.py rpii:/home/pi
echo 'Uploaded to Ryan PI 2'
scp ./main/client.py ./main/pinio.py peng:/home/pi
echo 'Uploaded to Penguinator PI'
scp ./main/client.py ./main/pinio.py alex:/home/pi
echo 'Uploaded to Alex PI'
scp ./main/client.py ./main/pinio.py matt:/home/pi
echo 'Uploaded to Matt PI'
