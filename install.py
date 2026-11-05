import os
import sys
import glob
import shutil
def find_chimerax_site_packages():
    candidates = []
    if sys.platform == "win32":
        local_app = os.environ.get("LOCALAPPDATA", os.path.expanduser(r"~\AppData\Local"))
        pattern = os.path.join(local_app, "UCSF", "ChimeraX", "*", "Python*", "site-packages")
        candidates.extend(glob.glob(pattern))
    elif sys.platform == "darwin":
        pattern = os.path.expanduser("~/Library/Application Support/ChimeraX/*/site-packages")
        candidates.extend(glob.glob(pattern))
    else:
        pattern = os.path.expanduser("~/.local/share/ChimeraX/*/site-packages")
        candidates.extend(glob.glob(pattern))
    return [p for p in candidates if os.path.isdir(p)]
def copy_directory_files(src_dir, dst_dir, allowed_exts=None):
    if not os.path.exists(src_dir):
        return 0
    os.makedirs(dst_dir, exist_ok=True)
    count = 0
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        target_root = dst_dir if rel == "." else os.path.join(dst_dir, rel)
        for fname in files:
            if allowed_exts and not fname.lower().endswith(allowed_exts):
                continue
            os.makedirs(target_root, exist_ok=True)
            shutil.copy2(os.path.join(root, fname), os.path.join(target_root, fname))
            count += 1
    return count
def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    start_dir = os.path.expanduser("~/chimerax_start")
    icons_dest_primary = os.path.expanduser("~/Downloads/chimerax_mac_icons")
    icons_dest_secondary = os.path.join(start_dir, "icons")
    os.makedirs(start_dir, exist_ok=True)
    src_theme = os.path.join(repo_root, "theme", "liquid_glass_theme.py")
    dst_theme = os.path.join(start_dir, "liquid_glass_theme.py")
    if os.path.exists(src_theme):
        shutil.copy2(src_theme, dst_theme)
    for folder in ("icons", "svg"):
        src_folder = os.path.join(repo_root, folder)
        copy_directory_files(src_folder, icons_dest_primary, (".png", ".svg"))
        copy_directory_files(src_folder, icons_dest_secondary, (".png", ".svg"))
    pth_line = (
        f"import sys, os; p = r'{start_dir}'; "
        f"sys.path.insert(0, p) if os.path.exists(p) and p not in sys.path else None; "
        f"import liquid_glass_theme\n"
    )
    site_packages_list = find_chimerax_site_packages()
    pkg_src = os.path.join(repo_root, "packages", "chimerax")
    for sp in site_packages_list:
        pth_path = os.path.join(sp, "mac_sequoia_theme.pth")
        with open(pth_path, "w", encoding="utf-8") as f:
            f.write(pth_line)
        if os.path.exists(pkg_src):
            copy_directory_files(pkg_src, os.path.join(sp, "chimerax"), (".png", ".svg"))
if __name__ == "__main__":
    main()
