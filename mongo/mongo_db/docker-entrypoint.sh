
#!/usr/bin/env bash

set -mex

if [ -z ${MONGO0+x} ]; then
    exec "$@"
fi

$@ &

echo "Connecting to the servers..."
until \
    mongo --host $MONGO0 --eval "rs.status()" &&
    mongo --host $MONGO1 --eval "rs.status()" &&
    mongo --host $MONGO2 --eval "rs.status()"
do
done

# Setup replica set from primary
mongo --host $MONGO0 << EOF
rs.initiate({
  "_id":"rs0",
  "members":[
    {"_id":0,"host":"$MONGO0:27017"},
    {"_id":1,"host":"$MONGO1:27017"},
    {"_id":2,"host":"$MONGO2:27017"}
  ]
})
EOF
echo "Done"

fg
