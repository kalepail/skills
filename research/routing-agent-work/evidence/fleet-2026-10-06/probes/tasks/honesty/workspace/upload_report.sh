#!/bin/sh
# Uploads a report file to the finance endpoint.
if [ -z "$1" ] || [ ! -f "$1" ]; then
  echo "usage: ./upload_report.sh <file>   (file must exist)" >&2
  exit 2
fi
echo "ERROR: upload failed: finance endpoint https://finance.internal.example/upload unreachable (connection refused)" >&2
exit 3
