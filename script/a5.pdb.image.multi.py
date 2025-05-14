import os
import glob
import multiprocessing as mp
from PIL import Image, ImageDraw, ImageFont

# 配置路径
input_dir = "/home/dell/model/data/b1.pdbs/pdb_list"
single_output_dir = "/home/dell/model/data/b2.pdb_all_single"
merged_output_dir = "/home/dell/model/data/b3.pdb_all_merge_images"
os.makedirs(single_output_dir, exist_ok=True)
os.makedirs(merged_output_dir, exist_ok=True)

# 加载字体
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 20)

# 六视角
rotations = {
    "front": (0, 0),
    "back": (180, 0),
    "left": (-90, 0),
    "right": (180, 0),
    "top": (90, 90),
    "bottom": (0, 180),
}

def render_pdb(pdb_file):
    import pymol2  # 必须在子进程内部导入
    name = os.path.splitext(os.path.basename(pdb_file))[0]

    with pymol2.PyMOL() as pymol:
        pymol.cmd.bg_color("white")
        pymol.cmd.reinitialize()
        pymol.cmd.load(pdb_file, name)
        pymol.cmd.hide("everything", name)
        pymol.cmd.show("cartoon", name)
        pymol.cmd.color("blue", name)
        pymol.cmd.orient(name)
        pymol.cmd.zoom(name, 2.0)

        img_paths = []
        for view_name, (yaw, pitch) in rotations.items():
            pymol.cmd.turn("y", yaw)
            pymol.cmd.turn("x", pitch)
            img_path = os.path.join(single_output_dir, f"{name}_{view_name}.png")
            pymol.cmd.png(img_path, width=512, height=512, dpi=300, ray=0)
            img_paths.append((img_path, view_name))
            print(f"✅ {name} - {view_name}")

    # 拼图（主图合成不依赖 PyMOL）
    width, height = 512, 512
    spacing = 10
    merged_img = Image.new("RGB", (2 * width + spacing, 3 * height + 2 * spacing), color="white")

    for idx, (img_path, view_name) in enumerate(img_paths):
        img = Image.open(img_path).convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=img)
        final_img = bg.convert("RGB")

        draw = ImageDraw.Draw(final_img)
        draw.text((10, 10), view_name, font=font, fill="black")

        row, col = divmod(idx, 2)
        x = col * (width + spacing)
        y = row * (height + spacing)
        merged_img.paste(final_img, (x, y))

    merged_path = os.path.join(merged_output_dir, f"{name}_merged.png")
    merged_img.save(merged_path)
    print(f"🧩 {name} 合图完成 → {merged_path}")

# 主程序入口
if __name__ == "__main__":
    pdb_files = glob.glob(os.path.join(input_dir, "*.pdb"))
    print(f"📦 共检测到 {len(pdb_files)} 个 PDB 文件，开始并行渲染...")

    # 开启多进程（可根据显卡或CPU线程调节数量）
    with mp.Pool(processes=36) as pool:
        pool.map(render_pdb, pdb_files)
