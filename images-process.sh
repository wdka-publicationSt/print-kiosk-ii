#!/bin/sh
dir=images
for img in $dir/*
do img_new_name=`echo "$img" | sed 's/\ /_/g'`
   mv "$img" "$img_new_name"
   echo "$img" "$img_new_name"
done
