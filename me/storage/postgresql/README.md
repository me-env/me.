# PostreSQL


### Install on ubuntu 20.04

````shell
sudo apt update ; sudo apt upgrade
sudo apt install postgresql postgresql-contrib
````

### Configuration

Connect to postgres user
````shell
sudo -i -u postgres
````

Start postgres server
````shell
service postgresql start
````

connect to psql shell
````shell
psql
````

````postgresql
ALTER USER postgres PASSWORD 'changeme'; -- Change password
CREATE USER me WITH CREATEDB NOCREATEROLE NOINHERIT NOSUPERUSER ENCRYPTED PASSWORD 'changmeaswell'; -- CREATE USER
````

Change login config from (file: pg_hba.conf   -    could be located in /etc/postgresql/12/main/)
````shell
local   all             postgres                                peer
local   all             all                                     peer
````
to
````shell
local   all             postgres                                md5
local   all             all                                     md5
````

Then restart the database
````shell
sudo service postgresql restart
````

Connect with user to me to db postgres
````shell
psql -U me -d postgres
````

Database me
````postgresql
CREATE DATABASE me WITH ENCODING 'UTF8'; -- FIXME set Collation & Locale
\c me -- Connect to me
\set ON_ERROR_STOP on -- ensure that the script stops running if it encounters an error
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO userName;
````

Schema me-banking
````postgresql
CREATE SCHEMA me_banking;
````

### Utils & Some basic tools

````postgresql
\dg -- list roles
\dn -- list schemas
\l -- list databases
\conninfo -- current user / db
\c [db] -- connect to db [db]
\c [db] [user] -- connect to db [db] to user [user]
\q -- quit
SELECT current_user, current_database(), current_schema;
SELECT schema_name FROM information_schema.schemata; -- List schemas
select column_name, data_type from information_schema.columns where table_schema = 'me_banking' AND table_name = 'transactions' ORDER BY ordinal_position; -- Get informations about a table
````

````shell
sudo service postgresql restart # Restart server (after config file modif for example)
/etc/init.d/postgresql reload # Might also be needed after config change
````


#### Links

https://www.enterprisedb.com/postgres-tutorials/postgresql-replication-and-automatic-failover-tutorial
https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart-fr
https://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge


