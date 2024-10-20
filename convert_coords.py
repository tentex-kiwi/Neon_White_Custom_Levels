import sys
from coord_finder import calculate_local_position  # Adjust import based on your script

if __name__=="__main__":
    if len(sys.argv) == 11:
        parent_coords = tuple(map(float, sys.argv[1:4]))
        parent_rotation = tuple(map(float, sys.argv[4:8]))
        to_coords = tuple(map(float, sys.argv[8:11]))
        print(f"Parent coordinates: {parent_coords}"
              f"\nParent rotation (quaternion): {parent_rotation}"
                f"\nTarget absolute coordinates: {to_coords}")
        x, y, z = calculate_local_position(to_coords, parent_coords, parent_rotation)
        print(f"Local coordinates: X={x}, Y={y}, Z={z}")
    else:
        print("Usage: python convert_coords.py x1 y1 z1 x2 y2 z2 w2 x3 y3 z3")