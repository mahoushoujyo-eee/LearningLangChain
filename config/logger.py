import logging
import sys

# 创建 logger 实例
logger = logging.getLogger("langchain_app")
logger.setLevel(logging.INFO)

# 避免重复添加 handler
if not logger.handlers:
    # 控制台输出
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(
        logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(console)

# 关闭 propagate，防止日志重复
logger.propagate = False