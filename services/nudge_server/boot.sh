#! bin/sh

exec hypercorn -b 0.0.0.0:9000 server:app