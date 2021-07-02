#!/bin/sh

uvicorn apis.business_api_server:app --reload

exec $SHELL