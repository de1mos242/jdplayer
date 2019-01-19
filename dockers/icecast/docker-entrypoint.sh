#!/bin/sh

if [ -n "$ICECAST_SOURCE_PASSWORD" ]; then
    echo apply ICECAST_SOURCE_PASSWORD $ICECAST_SOURCE_PASSWORD
    sed -i "s/<source-password>[^<]*<\/source-password>/<source-password>$ICECAST_SOURCE_PASSWORD<\/source-password>/g" /etc/icecast.xml
fi
if [ -n "$ICECAST_RELAY_PASSWORD" ]; then
    echo apply ICECAST_RELAY_PASSWORD $ICECAST_RELAY_PASSWORD
    sed -i "s/<relay-password>[^<]*<\/relay-password>/<relay-password>$ICECAST_RELAY_PASSWORD<\/relay-password>/g" /etc/icecast.xml
fi
if [ -n "$ICECAST_ADMIN_PASSWORD" ]; then
    echo apply ICECAST_ADMIN_PASSWORD $ICECAST_ADMIN_PASSWORD
    sed -i "s/<admin-password>[^<]*<\/admin-password>/<admin-password>$ICECAST_ADMIN_PASSWORD<\/admin-password>/g" /etc/icecast.xml
fi
if [ -n "$ICECAST_ADMIN_USERNAME" ]; then
    echo apply ICECAST_ADMIN_USERNAME $ICECAST_ADMIN_USERNAME
    sed -i "s/<admin-user>[^<]*<\/admin-user>/<admin-user>$ICECAST_ADMIN_USERNAME<\/admin-user>/g" /etc/icecast.xml
fi
if [ -n "$ICECAST_ADMIN_EMAIL" ]; then
    echo apply ICECAST_ADMIN_EMAIL $ICECAST_ADMIN_EMAIL
    sed -i "s/<admin>[^<]*<\/admin>/<admin>$ICECAST_ADMIN_EMAIL<\/admin>/g" /etc/icecast.xml
fi
if [ -n "$ICECAST_LOCATION" ]; then
    echo apply ICECAST_LOCATION $ICECAST_LOCATION
    sed -i "s/<location>[^<]*<\/location>/<location>$ICECAST_LOCATION<\/location>/g" /etc/icecast.xml
fi
if [ -n "$ICECAST_HOSTNAME" ]; then
    echo apply ICECAST_HOSTNAME $ICECAST_HOSTNAME
    sed -i "s/<hostname>[^<]*<\/hostname>/<hostname>$ICECAST_HOSTNAME<\/hostname>/g" /etc/icecast.xml
fi
if [ -n "$ICECAST_MAX_CLIENTS" ]; then
    echo apply ICECAST_MAX_CLIENTS $ICECAST_MAX_CLIENTS
    sed -i "s/<clients>[^<]*<\/clients>/<clients>$ICECAST_MAX_CLIENTS<\/clients>/g" /etc/icecast.xml
fi
if [ -n "$ICECAST_MAX_SOURCES" ]; then
    echo apply ICECAST_MAX_SOURCES $ICECAST_MAX_SOURCES
    sed -i "s/<sources>[^<]*<\/sources>/<sources>$ICECAST_MAX_SOURCES<\/sources>/g" /etc/icecast.xml
fi

exec "$@"