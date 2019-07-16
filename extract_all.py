import os
from multiprocessing import Pool, cpu_count



root_path = '/home/ros/Downloads/czx/tesla/bags_0514'
out_path = '/home/ros/Downloads/bags'

bags = []
for scene in os.listdir(root_path):
    print(scene)
    scene_path = root_path + '/' + scene
    if '.bag' in str(scene):
        bags.append(scene_path)
        continue
    for data in os.listdir(scene_path):
        data_path = scene_path + '/' + data
        if '.bag' in str(data):
            bags.append(data_path)
            continue
        
        for fi in os.listdir(data_path):
            file_path = data_path + '/' + fi
            print(file_path)
            if '.bag' in str(fi):
                bags.append(file_path)
                continue
cmd_list = []
cmds = ''
for bag in bags:
    print(bag)
    bag_name = bag.split('/')[-1][0:-4]
    print(bag_name)
    out_folder = out_path + '/' + bag_name
    if not os.path.isdir(out_folder):
        os.makedirs(out_folder)
    out_file = out_folder+'.mp4'
    cmd = 'python video_extract.py extract ' + bag + ' 0 ' + out_file
    cmds += (cmd + '  &\n')
    cmd_list.append(cmd)
    print(cmd)


for i in range(len(cmd_list)-1):
    print(cmd_list[i])
    os.system(cmd_list[i])
