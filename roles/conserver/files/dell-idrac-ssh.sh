#!/bin/sh
set -u

HOST="$1"
USER="$2"
PASS="$3"

# Handle IPv6 addresses by wrapping in brackets
case "$HOST" in
  *:*)
    SSH_HOST="[$HOST]"
    ;;
  *)
    SSH_HOST="$HOST"
    ;;
esac

SSHPASS="$PASS" exec sshpass -e ssh \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -o LogLevel=ERROR \
  -l "$USER" \
  "$SSH_HOST" \
  'console com2'
