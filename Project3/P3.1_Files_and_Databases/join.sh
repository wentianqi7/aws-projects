#!/bin/bash

join -t , -1 1 -2 1 <(sort million_songs_sales_data.csv) <(sort million_songs_metadata.csv) > million_songs_metadata_and_sales.csv
