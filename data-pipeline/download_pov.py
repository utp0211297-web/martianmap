# -*- coding: utf-8 -*-
"""
download_pov.py
Baja fotos POV de Curiosity desde el servidor publico de MSL.
Sols 387, 400, 412, 420 — Navcam y Mastcam.
"""
import os, sys, json, urllib.request, re
os.chdir(os.path.dirname(os.path.abspath(__file__)))

OUT_DIR = "pov_raw"
os.makedirs(OUT_DIR, exist_ok=True)

# URLs directas conocidas de Navcam y Mastcam en esos sols
# Formato: (sol, camara, url, descripcion)
FOTOS = [
    # Sol 387 - Navcam
    (387, "NAVCAM", "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00387/opgs/edr/ncam/NLB_406033631EDR_F0150000NCAM00353M_.JPG", "Navcam izquierda Sol 387"),
    (387, "NAVCAM", "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00387/opgs/edr/ncam/NRB_406033631EDR_F0150000NCAM00353M_.JPG", "Navcam derecha Sol 387"),
    # Sol 400 - Navcam
    (400, "NAVCAM", "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00400/opgs/edr/ncam/NLB_407332623EDR_F0160704NCAM00302M_.JPG", "Navcam izquierda Sol 400"),
    # Sol 412 - Mastcam
    (412, "MASTCAM", "https://mars.nasa.gov/msl-raw-images/msss/00412/mcam/0412MR0017510000401723E01_DXXX.jpg", "Mastcam derecha Sol 412"),
    (412, "MASTCAM", "https://mars.nasa.gov/msl-raw-images/msss/00412/mcam/0412ML0017510000104869E01_DXXX.jpg", "Mastcam izquierda Sol 412"),
    (412, "NAVCAM",  "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00412/opgs/edr/ncam/NLB_408532669EDR_F0162900NCAM00320M_.JPG", "Navcam Sol 412 A"),
    (412, "NAVCAM",  "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00412/opgs/edr/ncam/NLB_408532669EDR_F0162900NCAM00318M_.JPG", "Navcam Sol 412 B"),
    # Sol 420 - Navcam
    (420, "NAVCAM",  "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00420/opgs/edr/ncam/NLB_409272926EDR_F0163888NCAM00320M_.JPG", "Navcam Sol 420 A"),
    (420, "NAVCAM",  "https://mars.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00420/opgs/edr/ncam/NLB_409272926EDR_F0163888NCAM00318M_.JPG", "Navcam Sol 420 B"),
    (420, "MASTCAM", "https://mars.nasa.gov/msl-raw-images/msss/00420/mcam/0420MR0018000000402099E01_DXXX.jpg", "Mastcam Sol 420"),
]

downloaded = []
failed = []

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; MARSWALK-hackathon/1.0)"
}

for sol, cam, url, desc in FOTOS:
    ext  = url.split(".")[-1].lower()
    fname = f"sol{sol:04d}_{cam}_{os.path.basename(url)}"
    fpath = os.path.join(OUT_DIR, fname)

    if os.path.exists(fpath) and os.path.getsize(fpath) > 10000:
        print(f"  ya existe {fname}")
        downloaded.append({"file": fname, "sol": sol, "camera": cam, "url": url, "description": desc})
        continue

    print(f"Descargando Sol {sol} {cam}: {os.path.basename(url)} ...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if len(data) < 5000:
            print(f"  SKIP: respuesta muy pequena ({len(data)} bytes) — URL invalida")
            failed.append(url)
            continue
        with open(fpath, "wb") as f:
            f.write(data)
        print(f"  OK {fname} ({len(data)//1024} KB)")
        downloaded.append({"file": fname, "sol": sol, "camera": cam, "url": url, "description": desc})
    except Exception as e:
        print(f"  ERROR: {e}")
        failed.append(url)

print(f"\nDescargadas: {len(downloaded)}  Fallidas: {len(failed)}")
with open("pov_index.json", "w") as f:
    json.dump(downloaded, f, indent=2)
print("Indice guardado: pov_index.json")
if failed:
    print("URLs fallidas:")
    for u in failed:
        print(f"  {u}")
