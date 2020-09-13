# README #

### Install common dev dependencies

```
pip3 install -r requirements.txt
pre-commit install
```

### Setup environment variables
```
cp setenv.sh.example setenv.sh
source setenv.sh
```
## Generate firebase config
```
python sellitback_notifier/manage.py generate_firebase_config conf/firebase_admin_service_file.json.j2 $SELLITBACK_FIREBASE_SERVICE_FILE
```
