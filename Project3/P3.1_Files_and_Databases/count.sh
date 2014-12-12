#!/bin/bash

artist_name="michael jackson"
start_year=1976
end_year=1992
n=0

cat million_songs_metadata.csv | while read line
do
  IFS=',' read -a arr <<< "$line"
  name=${arr[6]}
  declare -l name
  name=$name
  #echo $name
  if [[ "${name}" == *$artist_name* ]] && [ ${arr[10]} -ge ${start_year} -a ${arr[10]} -le ${end_year} ]
  then 
    n=$(($n+1))
    echo $n
  fi
done
