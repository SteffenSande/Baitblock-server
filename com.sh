#!/bin/bash

gunicorn NewsEnhancer.wsgi:application --bind 165.227.136.59:8001
