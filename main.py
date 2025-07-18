from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from api.chat import router as chat_router
import config.my_nacos as nacos
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging, coloredlogs

#1. 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()]
)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

coloredlogs.install(
    level='INFO',
    fmt='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

#2. nacos生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    server_addresses = "127.0.0.1"
    port = 8000
    service_name = "langchain-service"
    group = "DEFAULT_GROUP"
    client = nacos.register_service(service_name, server_addresses, port, group)

    # 创建心跳调度器
    sched = AsyncIOScheduler(timezone="Asia/Shanghai")
    sched.add_job(
        lambda: client.send_heartbeat(service_name, server_addresses, port, group),
        "interval",
        seconds=5,
        max_instances=1,
    )
    sched.start()
    app.state.sched = sched          # 保存到 app.state，供全局访问

    yield  # 应用开始接受请求

    app.state.sched.shutdown(wait=False)
    nacos.deregister_service(service_name, server_addresses, port)

#3. fastapi配置
app = FastAPI(
    title="LearningLangChain",
    version="0.1.0",
    description="基于LangChain的AI应用",
    lifespan=lifespan
)

app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "Hello from LearningLangChain!"}
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def main():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()