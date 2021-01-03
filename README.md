# README #


### Install pipenv:

```
pip3 install pipenv
```

### Install common dev dependencies

```
cd /home/hos-backend/house-of-souls-api/house_of_souls
pipenv install
```

### Start gunicorn manually (Full process):
```
ssh root@ip_address
su - hos-backend
cd /home/hos-backend/house-of-souls-api
pipenv shell
cd house_of_souls/
gunicorn house_of_souls.wsgi:application   \
    --name "house-of-souls"   \
    --workers 3   \
    --user="hos-backend"    \
    --group="hos-backend"   \
    --bind=unix:/home/hos-backend/run/gunicorn.sock   \
    --log-level=error   \
    --log-file=-
```

### Start/Restart the app using supervisor:
```
sudo supervisorctl start house-of-souls
sudo supervisorctl restart house-of-souls
```

### Check the app status using supervisor:
```
sudo supervisorctl status house-of-souls
```

### Update the app. (Full process):
```
ssh root@ip_address
su - hos-backend
cd house-of-souls-api/house_of_souls
git pull --rebase
python3 house_of_souls/manage.py collectstatic
python3 house_of_souls/manage.py migrate
exit
sudo supervisorctl restart house-of-souls
exit
```
