#!/bin/bash
make extract
cd source_code
make all
cd ../
make clean
logout
