import os
import shutil

def copystatic(src, dst):
    # 1. If dst exists, delete it
    if os.path.exists(dst):
        shutil.rmtree(dst)

    # 2. Create dst
    os.makedirs(dst, exist_ok=True)

    # 3. Loop over everything in src
    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isfile(src_path):
            # copy a single file
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            # recursively copy a directory
            copystatic(src_path, dst_path)