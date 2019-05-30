#!/bin/sh
dir=../images
for img in $dir/*
do mogrify -depth 8 -colorspace GRAY -ordered-dither h4x4a "$img" 
    # img_new_name=`echo "$img" | sed 's/\ /_/g'`
   # mv "$img" "$img_new_name"
    # echo "$img" "$img_new_name"
done
