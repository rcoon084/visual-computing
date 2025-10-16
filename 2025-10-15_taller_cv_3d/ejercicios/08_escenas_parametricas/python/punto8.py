from vedo import Sphere, Cube, Cone, Cylinder, show, merge
import json
import trimesh

input_file = "scene_parametrica.obj"
output_file = "scene_parametrica.gltf"

data = [
    {"type": "sphere", "pos": [0, 0, 0], "r": 0.5, "color": "red"},
    {"type": "cube", "pos": [2, 0, 0], "size": 0.8, "color": "blue"},
    {"type": "cone", "pos": [-2, 0, 0], "r": 0.6, "h": 1.2, "color": "green"},
    {"type": "cylinder", "pos": [0, 2, 0], "r": 0.4, "h": 1.0, "color": "orange"},
    
]

actors = []
for obj in data:
    t = obj["type"]
    if t == "sphere":
        mesh = Sphere(r=obj["r"], c=obj["color"]).pos(obj["pos"])
    elif t == "cube":
        mesh = Cube(side=obj["size"], c=obj["color"]).pos(obj["pos"])
    elif t == "cone":
        mesh = Cone(r=obj["r"], height=obj["h"], c=obj["color"]).pos(obj["pos"])
    elif t == "cylinder":
        mesh = Cylinder(r=obj["r"], height=obj["h"], c=obj["color"]).pos(obj["pos"])
    actors.append(mesh)

show(actors, __doc__, bg='white', axes=1)

scene = merge(actors)
scene.write(r"ejercicios\08_escenas_parametricas\python\scene_parametrica.obj")
scene.write(r"ejercicios\08_escenas_parametricas\python\scene_parametrica.stl")

mesh = trimesh.load(r"ejercicios\08_escenas_parametricas\python\scene_parametrica.obj")
mesh.export(r"ejercicios\08_escenas_parametricas\python\scene_parametrica.glb")

print("✅ Escena generada y exportada (OBJ, STL, GLTF)")
