# FLOCX Marketplace

flocx-market is an OpenStack service for acting as a FLOCX marketplace to communicate with a FLOCX provider. [More details on FLOCX](https://cci-moc.github.io/flocx/)


### Installation

To  install the python code:

```
    $ git clone https://github.com/CCI-MOC/flocx-market.git
    $ cd flocx-market
    $ sudo python setup.py install
    $ pip install -r requirements.txt
```


### Configuration

Run the following to generate the configuration file and copy it to the right place:

```
    $ tox -egenconfig
    $ sudo mkdir /etc/flocx-market
    $ sudo cp etc/flocx-market/flocx-market.conf.sample /etc/flocx-market/flocx-market.conf
```

Edit `/etc/flocx-market/flocx-market.conf` with the proper values. Some useful values include:

```
[DEFAULT]

debug=True
log_dir=/var/log/flocx-market

[database]
connection=<db connection string>

[keystone_authtoken]
www_authenticate_uri=<public Keystone endpoint>
auth_type=password
auth_url=<keystone auth URL>
username=admin
password=<password>
user_domain_name=Default
project_name=admin
project_domain_name=Default
```


### Run the Services

Start by instantiatiating the database:

```
    $ flocx-market-dbsync
```

Once that's done, you can run the manager and API services:


```
    $ flocx-market-manager
    $ flocx-market-api
```


### Service catalog
#### Create the services

```
openstack service create --name flocx-market --description flocx-market marketplace
```

#### Register the services at an endpoint

```
openstack endpoint create flocx-market public http://example.com:XXXX
```

#### Create service users

Create a project for the service users:

```
openstack project create service --domain default
```

Create service users for the relevant services:

```
openstack user create flocx-market --password PASSWORD
```

Assign the admin role to the user-project pair:

```
openstack role add --project service --user flocx-market admin
```
