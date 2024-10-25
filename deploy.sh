#!/bin/bash
# exit on any kind of error
set -e
echo " - Delete old files"
find /home/ubuntu/project/certificate/ -type f ! -path '*/logs/*' ! -path '*/backup/*' ! -path '*/media/*' ! -name '*backup*'! -name '.env' -delete && find /home/ubuntu/project/certificate/ -depth -type d -empty -delete
echo " - Copy new files"
rsync -av * /home/ubuntu/project/certificate/ --exclude=.git
rsync -av prospector.yml /home/ubuntu/project/certificate/ # Strange, but this faile is excluded and adding it to include also does not work
cd /home/ubuntu/project/certificate
echo " - Activate virtual env"
source ../qr_venv/bin/activate
echo " - Installing dependencies"
pip install -r /home/ubuntu/project/certificate/req.txt --upgrade
# $1 boolean from what depends if dev or prod config
if $1 ; then
    # for dev install dev requirements
    pip install -r /home/ubuntu/project/certificate/requirements_dev.txt --upgrade
fi
echo " - Manage"
./manage.py migrate >/dev/null
./manage.py collectstatic --noinput>/dev/null
if $1 ; then
    # for dev run unittests and prospector
    ./manage.py test
    prospector
fi
deactivate
echo " - Restart gunicorn"
sudo cp /home/django/uzgrant2021/configs/uzgrant2021.gunicorn.service /etc/systemd/system/certificate
sudo systemctl daemon-reload
sudo systemctl enable uzgrant2021.gunicorn.service
sudo systemctl restart uzgrant2021.gunicorn.service
