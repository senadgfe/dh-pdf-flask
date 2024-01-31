import bpy

# Get the current scene
scene = bpy.context.scene

show_layers = ["Kamera", "Lights"]


def generate_view_layers():
    # Iterate through collections in the scene
    for collection in bpy.context.scene.view_layers[0].layer_collection.children:
        if 'x' in collection.name.lower():
            view_layer_name = collection.name

            # Check if the view layer already exists
            if view_layer_name not in bpy.context.scene.view_layers:
                # Create a new view layer
                new_view_layer = bpy.context.scene.view_layers.new(name=view_layer_name)


def change_collection_visibility():
    for view_layer in bpy.context.scene.view_layers:
        for view_collection in view_layer.layer_collection.children:
            if view_collection.name == view_layer.name or view_collection.name in show_layers:
                    view_collection.exclude = False
            else:
                    view_collection.exclude = True


generate_view_layers()
change_collection_visibility()

print("Script execution complete.")
