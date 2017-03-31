FROM postgres:9.6

COPY remote_connections.sh /docker-entrypoint-initdb.d/
RUN chmod 755 /docker-entrypoint-initdb.d/remote_connections.sh
COPY init.sql /docker-entrypoint-initdb.d/
