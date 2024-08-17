#! /bin/bash
set -e

RENDER_SERVICE_ID="${RENDER_SERVICE_ID}"
RENDER_API_KEY="${RENDER_API_KEY}"

curl --request POST \
     --url https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys \
     --header "accept: application/json" \
     --header "authorization: Bearer $RENDER_API_KEY" \
     --header "content-type: application/json"