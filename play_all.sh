#!/bin/bash

for file in ./$1/*

do
	echo $file
	if test -f $file
	then
		echo $file
		rosbag play $file --topic /navi/fusion /sensor/cameraF50/image_raw/compressed /sensor/cameraRF100/image_raw/compressed /sensor/cameraLF100/image_raw/compressed /sensor/cameraLR100/image_raw/compressed /sensor/cameraRR100/image_raw/compressed /sensor/cameraR50/image_raw/compressed /whoami /velodyne_multi_scans /sensor/gpfpd --clock
	fi
	sleep 1
done
