#!/bin/bash

# Encuentra todas las carpetas llamadas __pycache__ y elimínalas
sudo find . -type d -name "__pycache__" -exec rm -rf {} +