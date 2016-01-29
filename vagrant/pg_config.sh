apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
apt-get -qqy install python-dev
apt-get -qqy install libmagickwand-dev npm git nodejs-legacy
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
pip install redis
pip install passlib
pip install itsdangerous
pip install flask-httpauth
pip install flask-login
pip install rauth
pip install flask-seasurf
pip install wtforms
pip install awesome-slugify
pip install SQLAlchemy-ImageAttach

su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb catalog'
su postgres -c 'psql -f /vagrant/catalog/catalog.sql'
su vagrant -c 'createdb'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd

npm install -g bower

cd /vagrant/catalog/app/static
su vagrant -c 'bower install'

cd ../../
python ./application.py
