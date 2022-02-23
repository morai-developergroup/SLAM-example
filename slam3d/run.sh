#!/bin/bash
docker run --net=host -it --rm \
            -v $(realpath ..):/root/catkin_ws/src/SLAM-example/SC-LeGO-LOAM/LeGO-LOAM \
            -w /root/catkin_ws/src/SLAM-example/SC-LeGO-LOAM/LeGO-LOAM \
            $@ \
            lego_loam
