# -*- coding: utf-8 -*-
import os, json, shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))

POV_DIR = "../Frontend/martianmap/public/data/gale/pov"
files = sorted(os.listdir(POV_DIR))

index = []
for i, fname in enumerate(files):
    if not fname.lower().endswith(".jpg"):
        continue

    # Determinar camara desde el nombre original
    if "ML" in fname:
        cam = "MASTCAM_LEFT"
    elif "MR" in fname:
        cam = "MASTCAM_RIGHT"
    else:
        cam = "MASTCAM"

    # Nombre limpio
    new_name = f"pov_{i+1:02d}_{cam.lower()}.jpg"
    old_path = os.path.join(POV_DIR, fname)
    new_path = os.path.join(POV_DIR, new_name)

    shutil.move(old_path, new_path)
    print(f"  {fname[:40]}... -> {new_name}")

    index.append({
        "file":        new_name,
        "url":         f"/data/gale/pov/{new_name}",
        "sol":         5073,
        "camera":      cam,
        "description": f"Mastcam Sol 5073 — zona boxwork Mount Sharp"
    })

# Guardar indice
index_path = os.path.join(POV_DIR, "index.json")
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

print(f"\nOK {len(index)} fotos renombradas")
print(f"Indice guardado: {index_path}")
