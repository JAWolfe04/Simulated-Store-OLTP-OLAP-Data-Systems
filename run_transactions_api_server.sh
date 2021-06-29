#!/bin/sh

uvicorn apis.transactions_api_server:app --reload

exec $SHELL