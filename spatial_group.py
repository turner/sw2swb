import numpy as np
from utils import to_float

def single_point_group_harvest_xyz(group, xyz, index):
    xyz_stack = np.column_stack((xyz[1], xyz[2], xyz[3]))
    dataset_name = str(index)
    print('Create dataset {:}'.format(dataset_name))
    group.create_dataset(dataset_name, data=xyz_stack)


def create_single_point_group(spatial_position_group, spacewalk_file):
    print('Create Ball & Stick Spatial Group')
    single_point_group = spatial_position_group.create_group('single_point')
    indices = []
    xyz_list = None
    for line in spacewalk_file:
        tokens = line.split()
        if 'trace' == tokens[0]:
            indices.append(int(tokens[1]))
            if xyz_list is not None:
                single_point_group_harvest_xyz(single_point_group, xyz_list, indices[-2])
                xyz_list = None
        elif 6 == len(tokens):
            if xyz_list is None:
                key = '%'.join([tokens[0], tokens[1], tokens[2]])
                xyz_list = [key, [], [], []]
            xyz_list[1].append(to_float(tokens[3]))
            xyz_list[2].append(to_float(tokens[4]))
            xyz_list[3].append(to_float(tokens[5]))
    return [xyz_list, indices, single_point_group]

def create_multi_point_group(cndbf, spatial_position_group, spacewalk_file):
    print('Create Pointcloud Spatial Group')
    multi_point_group = spatial_position_group.create_group('multi_point')

def create_spatial_group(cndbf, root, spacewalk_file, args):
    spatial_position_group = root.create_group('spatial_position')
    if args.single_point:
        result = create_single_point_group(spatial_position_group, spacewalk_file)
        xyz = result[0]
        indices = result[1]
        single_point_group = result[2]

        # harvest last dataset
        single_point_group_harvest_xyz(single_point_group, xyz, indices[-1])
    elif args.multi_point:
        create_multi_point_group(cndbf, spatial_position_group, spacewalk_file)

    return None