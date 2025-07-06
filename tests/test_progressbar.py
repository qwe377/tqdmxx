import time
from tqdmxx import tqdmxx

# 创建一个经典样式的进度条
bar = tqdmxx(total=100, style="classic", color="green")

# 更新进度
for i in range(100):
    time.sleep(0.05)
    bar.update()

# 完成进度条
bar.finish()