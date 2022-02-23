#!/bin/bash
docker run --net=host -it --rm \
            -v $(realpath ..):/root/catkin_ws/src/SLAM-example/lidar2d_mapping \
            -w /root/catkin_ws/src/SLAM-example/lidar2d_mapping \
            $@ \
            lidar2d_mapping
