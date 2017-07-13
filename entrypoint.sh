#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        exec python main.py
        ;;
    test)
        echo "Test (not yet)"
        ;;
    start)
        echo "Running Start"
        exec gunicorn -c gunicorn.py rasdaman-stats:app
        ;;
    *)
        exec "$@"
esac
