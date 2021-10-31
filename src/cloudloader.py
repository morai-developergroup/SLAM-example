import os
import numpy as np
import open3d as o3d
import math
import re

class cloudLoader:
    def __init__(self, config=None):
        self.cfg = config
        self.data_path = config['PATH']['DATA']
        self.lidar_list = [file for file in os.listdir(os.path.join(self.data_path, config['LIDAR1']['PATH'])) if file.endswith(".bin")]
        self.lidar_list.sort(key=self.sort_func)
        
        self.dual = config['LIDAR']['DUAL']
        self.thres_mode = config['LIDAR']['THRES']
        self.noise = config['LIDAR']['NOISE']
        
        if (self.thres_mode):
            self.range = config['LIDAR']['RANGE']
        if (self.dual):
            self.lidar1_path = os.path.join(self.data_path, config['LIDAR1']['PATH'])
            self.lidar1_transform = self.get_SE3(config['LIDAR1']['TRANSFORM'])
            
            self.lidar2_path = os.path.join(self.data_path, config['LIDAR2']['PATH'])
            self.lidar2_transform = self.get_SE3(config['LIDAR2']['TRANSFORM'])
        else:
            self.lidar_path = os.path.join(self.data_path, config['LIDAR1']['PATH'])
            self.lidar_transform = self.get_SE3(config['LIDAR1']['TRANSFORM'])

    def __len__(self):
        return len(self.lidar_list)
    
    def __getitem__(self, index):
        if (self.dual):
            return self.bin2cloud(os.path.join(self.lidar1_path, self.lidar_list[index])).transform(self.lidar1_transform) \
                + self.bin2cloud(os.path.join(self.lidar2_path, self.lidar_list[index])).transform(self.lidar2_transform)
        else:
            return self.bin2cloud(os.path.join(self.lidar_path, self.lidar_list[index])).transform(self.lidar1_transform)
    
    def sort_func(self, file):
        return int(re.sub(r'[^0-9]', '', file))   

    def bin2cloud(self, bin_file):
        
        cloud_data = np.fromfile(bin_file, dtype=np.float32).reshape((-1,4))
        
        # Check empty
        open3d_cloud = o3d.geometry.PointCloud()
        if len(cloud_data)==0:
            print("Converting an empty cloud")
            return None

        if (self.thres_mode):
            scan_ranges = np.linalg.norm(cloud_data[:,:3], axis = 1)
            roi_ids = np.where((scan_ranges > self.range[0]) & (scan_ranges < self.range[1]))
            cloud_data = cloud_data[roi_ids[0],:]

        scan_int = np.zeros((len(cloud_data),3))
        scan_int[:,0] = cloud_data[:,3]

        if self.noise > 0:
            noise = np.random.normal(0, self.noise, cloud_data[:,:3].shape)
            cloud_data[:,:3] = cloud_data[:,:3] + noise

        # combine
        open3d_cloud.points = o3d.utility.Vector3dVector(cloud_data[:,:3])
        open3d_cloud.colors = o3d.utility.Vector3dVector(scan_int)

        return open3d_cloud

    def get_SE3(self, transform):
        T = np.eye(4)
        T[:3, :3] = self.get_SO3(transform[3:])
        T[:3, 3] = transform[:3]
        
        return T
    def get_SO3(self, RPY):
        rot_x = self.rotx(RPY[0])
        rot_y = self.roty(RPY[1])
        rot_z = self.rotz(RPY[2])
        return  rot_z @ rot_y @ rot_x

    def rotx(self, angle):
        angle *= math.pi/180
        return np.array([
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]])

    def roty(self, angle):
        angle *= math.pi/180
        return np.array([
            [math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)]])
        
    def rotz(self, angle):
        angle *= math.pi/180
        return np.array([
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]])
        
    def visualize(self, index):
        if (self.dual):
            o3d.visualization.draw_geometries([self.bin2cloud(os.path.join(self.lidar1_path, self.lidar_list[index])).transform(self.lidar1_transform) \
                + self.bin2cloud(os.path.join(self.lidar2_path, self.lidar_list[index])).transform(self.lidar2_transform)])
        else:
            o3d.visualization.draw_geometries([self.bin2cloud(os.path.join(self.lidar_path, self.lidar_list[index])).transform(self.lidar_transform)])
     