import warnings
import os

from numpy import left_shift
from tqdm import tqdm
import open3d as o3d
import argparse
from src.cloudloader import cloudLoader
from src.poseloader import poseLoader
import yaml
warnings.filterwarnings(action='ignore')

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help="configuration file name")
    args = parser.parse_args()

    with open(os.path.join(os.getcwd(), 'config', args.config)) as f: 
        cfg = yaml.safe_load(f)
    
    poses = poseLoader(config=cfg)
    pcs = cloudLoader(config=cfg)

    print("len: ", len(pcs))
    align_pc = o3d.geometry.PointCloud()
    if (cfg['VISUALIZE']["ACTIVE_VIS"]):
        vis = o3d.visualization.Visualizer() 
        vis.create_window('Mapping', visible = True) 

    for i in tqdm(range(len(pcs))): #len(pcs)
        print("Cloud file: ", pcs.lidar_list[i])
        print("GPS file: ", poses.gps_list[i])
        print("IMU file: ", poses.imu_list[i])
        align_pc += pcs[i].transform(poses[i])
        print("cloud points: ", len(align_pc.points))
        if cfg['VISUALIZE']['ACTIVE_VIS']:
            if i ==0:
                vis.add_geometry(align_pc) 
            vis.update_geometry(align_pc)
            vis.poll_events()
            vis.update_renderer()
    
    if (cfg['MODEL']['SAVE_MODEL']):
        print("...................Saving 3D model.........................................")
        os.makedirs(cfg['PATH']['SAVE'], exist_ok=True)
        file_name = os.path.join(cfg['PATH']['SAVE'], cfg['MODEL']['MODEL_NAME'])
        align_pc = align_pc.voxel_down_sample(voxel_size=cfg['MODEL']['VOXEL_SIZE'])
        o3d.io.write_point_cloud(file_name, align_pc)
        print("Done.")
    
    if (cfg['VISUALIZE']['FINAL_VIS']):
        vis.destroy_window()
        o3d.visualization.draw_geometries([align_pc])
        


