import time
from nacos import NacosClient
from config.logger import logger as log

# 全局客户端实例
_nacos_client = None


def register_service(service_name, ip, port, group_name):
    """注册服务到Nacos"""
    global _nacos_client
    
    # Nacos 服务端地址 (注意这里应该是Nacos服务器的地址，不是当前服务的地址)
    nacos_server = "127.0.0.1:8848"  # Nacos服务器地址
    _nacos_client = NacosClient(server_addresses=nacos_server, namespace="public")
    log.info(f"Nacos SDK server_list:{_nacos_client.server_list}")

    _nacos_client.add_naming_instance(
        service_name=service_name,
        ip=ip,
        port=port,
        group_name=group_name,
        weight=1.0,
        metadata={"version": "1.0", "env": "dev"}
    )

    log.info(f"[Nacos] {service_name} registered at {ip}:{port}")
    return _nacos_client


def deregister_service(service_name, ip, port, group_name="DEFAULT_GROUP"):
    """从Nacos注销服务"""
    global _nacos_client
    
    if _nacos_client is None:
        log.error("[Nacos] No client available for deregistration")
        return
    
    try:
        _nacos_client.remove_naming_instance(
            service_name=service_name,
            ip=ip,
            port=port,
            group_name=group_name
        )
        log.info(f"[Nacos] {service_name} deregistered from {ip}:{port}")
    except Exception as e:
        log.error(f"[Nacos] Failed to deregister service: {e}")


def get_service_instances(service_name, group_name="DEFAULT_GROUP"):
    """获取服务实例列表"""
    global _nacos_client
    
    if _nacos_client is None:
        log.info("[Nacos] No client available")
        return []
    
    try:
        instances = _nacos_client.list_naming_instance(
            service_name=service_name,
            group_name=group_name
        )
        return instances.get('hosts', [])
    except Exception as e:
        log.error(f"[Nacos] Failed to get service instances: {e}")
        return []
