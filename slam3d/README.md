# SC-LeGO-LOAM

Original repository: https://github.com/irapkaist/SC-LeGO-LOAM

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