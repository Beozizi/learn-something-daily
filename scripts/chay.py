r"""Chạy một script trong đúng môi trường Python của máy này (đọc cau-hinh.json).

    py scripts\chay.py <vai> <script.py> [tham số…]

Ví dụ:
    py scripts\chay.py tts   scripts\long-tieng.py tap\<tập> --engine genmax ...
    py scripts\chay.py align scripts\can-phu-de.py tap\<tập> --lang en
    py scripts\chay.py media scripts\tach-nen.py <ảnh> --out tach-nen
    py scripts\chay.py chung scripts\do-khoang-trong.py tap\<tập>
"""
import os
import subprocess
import sys

import cau_hinh

if len(sys.argv) < 3 or sys.argv[1] not in cau_hinh.ROLES:
    sys.exit(__doc__ + f"\nVai hợp lệ: {', '.join(cau_hinh.ROLES)}")
role, *rest = sys.argv[1:]
py = cau_hinh.venv_python(role)
if not py.exists():
    sys.exit(f"Chưa có môi trường '{role}' ({py}). Chạy scripts\\cai-dat.ps1 hoặc sửa cau-hinh.json.")
sys.exit(subprocess.call([str(py), *rest], env=cau_hinh.setup_env(dict(os.environ))))
