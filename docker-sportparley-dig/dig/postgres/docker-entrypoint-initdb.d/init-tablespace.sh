#!/bin/bash
set -e

mkdir /var/lib/postgresql/data/db_tablespace/
chown postgres:postgres /var/lib/postgresql/data/db_tablespace/

mkdir /var/lib/postgresql/data/db_tablespace/ts_parley/
chown postgres:postgres /var/lib/postgresql/data/db_tablespace/ts_parley/

mkdir /var/lib/postgresql/data/db_tablespace/ts_comer/
chown postgres:postgres /var/lib/postgresql/data/db_tablespace/ts_comer/

mkdir /var/lib/postgresql/data/db_tablespace/ts_finance/
chown postgres:postgres /var/lib/postgresql/data/db_tablespace/ts_finance/

mkdir /var/lib/postgresql/data/db_tablespace/pwa_base/
chown postgres:postgres /var/lib/postgresql/data/db_tablespace/pwa_base/

mkdir /var/lib/postgresql/data/db_tablespace/com_default/
chown postgres:postgres /var/lib/postgresql/data/db_tablespace/com_default/

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE TABLESPACE ts_parley OWNER $POSTGRES_USER LOCATION '/var/lib/postgresql/data/db_tablespace/ts_parley/';
    CREATE TABLESPACE ts_comer OWNER $POSTGRES_USER LOCATION '/var/lib/postgresql/data/db_tablespace/ts_comer/';
    CREATE TABLESPACE ts_finance OWNER $POSTGRES_USER LOCATION '/var/lib/postgresql/data/db_tablespace/ts_finance/';
    CREATE TABLESPACE pwa_base OWNER $POSTGRES_USER LOCATION '/var/lib/postgresql/data/db_tablespace/pwa_base/';
    CREATE TABLESPACE com_default OWNER $POSTGRES_USER LOCATION '/var/lib/postgresql/data/db_tablespace/com_default/';
EOSQL