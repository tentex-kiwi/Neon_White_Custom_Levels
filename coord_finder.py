import math
import numpy as np
from scipy.spatial.transform import Rotation as R
import coordinates as c
import argparse

def quaternion_to_matrix(q):
    # Converts a quaternion (qx, qy, qz, qw) into a 3x3 rotation matrix
    r = R.from_quat([q[0], q[1], q[2], q[3]])
    return r.as_matrix()

def calculate_local_position(absolute_pos, parent_pos, parent_quat):
    # Step 1: Calculate the offset between the target absolute position and the parent's absolute position
    offset_world = np.array(absolute_pos) - np.array(parent_pos)
    
    # Step 2: Convert the parent quaternion to a rotation matrix
    parent_rotation_matrix = quaternion_to_matrix(parent_quat)
    
    # Step 3: Invert the parent's rotation matrix (transpose for an orthogonal matrix)
    parent_rotation_matrix_inv = np.linalg.inv(parent_rotation_matrix)
    
    # Step 4: Apply the inverse rotation to the world space offset to get the local position
    local_pos = np.dot(parent_rotation_matrix_inv, offset_world)
    
    return local_pos

def main(output_file=None):
    output = []
    print('starting')

    # Process each level, and store editor file along with the output message
    for level in sorted(c.custom_present_coordinates.keys()):
        coordinates = c.custom_present_coordinates[level]
        
        editor_file = c.in_game_level_to_level_file.get(level)
        if editor_file is None:
            output.append((None, f'{level} could not be found in the mapping to editor files. Please check spelling'))
            continue
        
        parent_coordinates = c.editor_present_parent_coordinates.get(editor_file)
        if parent_coordinates is None or parent_coordinates == (-1, -1, -1, 0):
            output.append((editor_file, f'{editor_file}\'s present does not exist or could not be found. Adding presents to levels that don\'t currently have one is not supported at the moment.'))
            continue
        
        parent_rotation = c.editor_present_parent_quaternion.get(editor_file)
        if parent_rotation is None or parent_rotation == (-1, -1, -1, 0):
            output.append((editor_file, f'{editor_file}\'s present does not exist or could not be found. Adding presents to levels that don\'t currently have one is not supported at the moment.'))
            continue
        
        x, y, z = calculate_local_position(coordinates, parent_coordinates, parent_rotation)
        output.append((editor_file, f'The updated coordinates to enter into the editor for {level}:\n file: {editor_file} X: {x}, Y: {y}, Z: {z}'))
    
    print('Done')

    # Sort output by editor file (the first element in each tuple)
    output.sort(key=lambda x: x[0])

    # Extract the messages and discard the editor file in the final output
    sorted_output = [msg for _, msg in output]

    if output_file:
        with open(output_file, 'w') as f:
            f.write('\n'.join(sorted_output))
        print(f'Output saved to {output_file}')
    else:
        print('\n'.join(sorted_output))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Run the main function with optional output file.")
    
    # Add the optional --output argument
    parser.add_argument('--output', type=str, help='Specify the output file name')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call main with the output file argument
    main(output_file=args.output)
