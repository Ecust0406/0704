#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 17:06:29 2019

@author: KONE
"""

import cv2
import rosbag
import numpy as np
import argparse
import sys
import os

def extract(bag_file, wanted_topic, save_file, framerate, start, end, every):
    bag = rosbag.Bag(bag_file, "r")
    writer = None

    items = os.path.splitext(save_file);
    save_path = items[0]
    save_format = items[1]
    if save_format == '.mp4':
        fourcc = 'X264'
    else:
        fourcc = 'DIVX'

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    try:
        for w_topic in wanted_topic:
            print "topic " + w_topic + " for " + bag_file
            w1_topic = "/sensor/" + w_topic + "/image_raw/compressed"
            cnt = 0
            part = 0

            for topic, msg, stamp in bag.read_messages(topics=[w1_topic]):
                img = cv2.imdecode(np.frombuffer(msg.data, dtype=np.uint8), 1)

                if writer == None:
                    name = "%s/%s_%02d%s" % (save_path, w_topic, part, save_format)
                    print "create video for " + name
		    if os.path.exists(name):
			print "exists " + name + "skip"
			break
                    writer = cv2.VideoWriter(
                        name, cv2.VideoWriter_fourcc(
                            *fourcc), framerate, (np.size(img, 1), np.size(img, 0)))
                    #f = open(name + '.timestamps', 'w')
                    f_msg = open(os.path.splitext(name)[0] + '.msg_timestamps', 'w')
                writer.write(img)

                cnt += 1
                if cnt % 100 == 0:
                    print "frame " + str(cnt)

              #  f.write("%.9lf\n" % (stamp.to_time()))
                f_msg.write("%.9lf\n" % (msg.header.stamp.to_time()))
                if every > 0 and cnt % every == 0:
                    writer = None
                    #f = None
                    f_msg = None
                    print name + " done"
                    part += 1
	    if writer is not None:
	        writer.release()
	        writer = None
	    
    except KeyboardInterrupt:
        pass

    print str(cnt) + " frames extracted"


def main():
    parser = argparse.ArgumentParser(description='extract video from rosbag')
    subparsers = parser.add_subparsers(dest='action')
    extract_parser = subparsers.add_parser('extract')
    extract_parser.add_argument('rosbag_file', type=str,
                                help='source rosbag file')
    extract_parser.add_argument('topic', type=str,
                                help='topic to extract')
    extract_parser.add_argument('save_file', type=str,
                                help='video to save')
    extract_parser.add_argument('--framerate', type=int, default=20,
                                help='framerate in fps (default: 20)')
    extract_parser.add_argument('--start', type=int, default=0, required=False,
                                help='start frame')
    extract_parser.add_argument('--end', type=int, default=-1, required=False,
                                help='end framers')
    extract_parser.add_argument('--every', type=int, default=-1, required=False,
                                help='split every N frames')

    args = parser.parse_args(sys.argv[1:])

    topics = [
        'camera_1a01', 'camera_1a00', 'camera_1a02', 'camera_1a03', 'camera_1a04', 'camera_1a05', 'camera_1a06',
        'camera_1a07', 'camera_2a00', 'camera_2a01', 'camera_2a02', 'camera_2a03', 'camera_2a04', 'camera_2a05',
        'camera_2a06', 'camera_2a07']
    topics = ['cameraF50', 'cameraLF100', 'cameraRF100', 'cameraR50', 'cameraLR100', 'cameraRR100']
    #topics = ['cameraR50', 'cameraLR100', 'cameraRR100']
    #topics = ['cameraF50']
    if args.action == 'extract':
        if args.topic != "0":
            topics = []
            topics.append(args.topic)
        extract(args.rosbag_file, topics, args.save_file, args.framerate, args.start, args.end, args.every)

if __name__ == '__main__':
    main()
