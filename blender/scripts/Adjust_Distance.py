import math

def adjust_camera_radius(object_bounds, camera_fov_degrees, current_camera_distance):
    # Calculate the diagonal size of the object's bounding box or sphere
    object_size = math.sqrt(sum(dim ** 2 for dim in object_bounds))

    # Calculate the desired distance based on the object size and camera FOV
    desired_distance = (object_size / 2) / math.tan(math.radians(camera_fov_degrees / 2))

    # Calculate the new circle radius
    new_circle_radius = desired_distance - current_camera_distance

    return new_circle_radius

# Usage
object_bounds = (object_width, object_height, object_depth)  # Replace with actual values
camera_fov_degrees = 60  # Replace with the camera's field of view
current_camera_distance = 5  # Replace with the current camera distance from the object's center

new_circle_radius = adjust_camera_radius(object_bounds, camera_fov_degrees, current_camera_distance)
