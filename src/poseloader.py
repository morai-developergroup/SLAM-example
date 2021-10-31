import os
import numpy as np
import re
import pyproj
class poseLoader:

    def __init__(self, config=None):
        self.cfg = config
        self.data_path = config['PATH']['DATA']
        self.imu_path = os.path.join(config['PATH']['DATA'], config['IMU']['PATH'])
        self.gps_path = os.path.join(config['PATH']['DATA'], config['GPS']['PATH'])
        self.imu_list = [file for file in os.listdir(self.imu_path) if file.endswith(".txt")]
        self.gps_list = [file for file in os.listdir(self.gps_path) if file.endswith(".txt")]
        self.imu_list.sort(key=self.sort_func)
        self.gps_list.sort(key=self.sort_func)
        
    def sort_func(self, file):
        return int(re.sub(r'[^0-9]', '', file))   
        
    def __len__(self):
        assert len(self.imu_list) == len(self.gps_list), 'list length is not same'
        return len(self.imu_list)
    
    def __getitem__(self, index):
        return self.get_SE3(index)

    def get_SE3(self, index):
        q = self.load_q(os.path.join(self.imu_path, self.imu_list[index]))
        gps = self.load_gps(os.path.join(self.gps_path, self.gps_list[index]))
        T = np.eye(4)
        T[:3, :3] = self.get_SO3(q)
        T[:3, 3] = self.gps2utm(gps)

        return T
    
    def load_q(self, fname):
        f = open(fname,'r')
        data = []
        for i, line in enumerate(f.readlines()):
            if i > 1:
                data.append(line.replace('\n','').split(' ')[3])
            if i == 5:
                break
        f.close()

        return list(map(float, data))
    
    def load_gps(self, fname):
        f = open(fname,'r')
        data = []
        for i, line in enumerate(f.readlines()):
            data.append(line.replace('\n','').split(' ')[2])
            if i ==4:
                break
        f.close()
        return list(map(float, data))
    
    def get_SO3(self, q):
        s = q[3]
        x = q[0]
        y = q[1]
        z = q[2]
        return np.array(
            [
                [1 - 2 * (y ** 2 + z ** 2), 2 * (x * y - s * z), 2 * (x * z + s * y)],
                [2 * (x * y + s * z), 1 - 2 * (x ** 2 + z ** 2), 2 * (y * z - s * x)],
                [2 * (x * z - s * y), 2 * (y * z + s * x), 1 - 2 * (x ** 2 + y ** 2)],
            ]
            )
        
    def gps2utm(self, gps):
        utm = pyproj.Proj(proj='utm', zone=52, ellps='WGS84', preserve_units=False)
        ll = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        x, y = pyproj.transform(ll, utm, gps[1], gps[0], radians=False)
        
        return round(x-gps[3],5), round(y-gps[4],5), round(gps[2],5) # offset
    

