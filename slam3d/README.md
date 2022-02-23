# 3D LiDAR SLAM EXAMPLE

This is a fork of the original [SC-LeGO-LOAM](https://github.com/irapkaist/SC-LeGO-LOAM).

The original author deserves all the credits, we just use simple fine-tuning practices to make the code more efficient in MORAI SIM.

## Docker install
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## Build
```bash
git clone https://github.com/morai-developergroup/SLAM-example.git
cd SLAM-example/slam3d
./build.sh
```

## Run

### On host:
```bash
roscore
```

```bash
cd SLAM-example/slam3d
rviz -d rviz.rviz
```

### On docker image:
```bash
cd SLAM-example/slam3d
./run.sh

roslaunch lego_loam run.launch
```