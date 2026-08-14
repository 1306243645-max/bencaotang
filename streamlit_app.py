"""妙手堂中医诊所 · Streamlit Cloud 部署版"""

import sys, os
from pathlib import Path

# 确保项目根目录在 path 中
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

# 设置工作目录
os.chdir(str(ROOT))

# 导入并运行 web app
# 注意: web/app.py 中的模块级 st.set_page_config 等会自动执行
from web.app import *

# 这个文件只需要被 streamlit run 即可
# Streamlit Cloud 会自动: streamlit run streamlit_app.py
