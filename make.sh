#!/bin/bash

IMAGE=$1
X=$2
Y=$3

mkdir -p tmp
for i in {1..240}; do
  printf -v FILE 'tmp/%04d.jpg' "$i"
  POINT=$((Y+ (i* 50)/240))
  convert $IMAGE -stroke brown -fill brown -draw "circle ${X}, ${Y}, ${X}, ${POINT}" $FILE
done

cd tmp
convert *.jpg movie.mpg
