apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-pip
su postgres -c 'createuser -dRS vagrant'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
