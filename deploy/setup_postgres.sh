#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly CREDENTIAL_FILE="./conf/local/credentials.yml"
readonly SQL_SETUP_FILE="./deploy/sql/postgres_data.sql"
readonly MODELLING_SCHEMA_FILE="./deploy/sql/modelling_schema.sql"

main() {
    if ! load_credentials; then
        log_error "Credentials could not be loaded"
        exit 1
    fi

    PGPASSWORD=${PG_PASSWORD} psql -U ${PG_USER} -h ${PG_HOST} -d ${PG_DATABASE} -p ${PG_PORT} -f ${SQL_SETUP_FILE}
    PGPASSWORD=${PG_PASSWORD} psql -U ${PG_USER} -h ${PG_HOST} -d ${PG_DATABASE} -p ${PG_PORT} -f ${MODELLING_SCHEMA_FILE}

}

load_credentials() {
    PG_DATABASE=$(cat ${CREDENTIAL_FILE} | ./env/bin/yq .db.pg_name | tr -d '""')
    PG_USER=$(cat ${CREDENTIAL_FILE} | ./env/bin/yq .db.pg_user | tr -d '""')
    PG_PASSWORD=$(cat ${CREDENTIAL_FILE} | ./env/bin/yq .db.pg_pass | tr -d '""')
    PG_HOST=$(cat ${CREDENTIAL_FILE} | ./env/bin/yq .db.pg_host | tr -d '""')
    PG_PORT=$(cat ${CREDENTIAL_FILE} | ./env/bin/yq .db.pg_port)
}

log_error() {
    printf '\e[31mERROR: %s\n\e[39m' "$1" >&2
}

 main
