import ssl
from celery import Celery
from app.core.config import settings

celery = Celery("enterpriserag", broker=settings.redis_url, backend=settings.redis_url, include=["app.workers.tasks"])

celery_conf = {
    "task_track_started": True,
    "task_time_limit": 1800,
    "task_soft_time_limit": 1700,
    "task_acks_late": True,
    "worker_prefetch_multiplier": 1,
    "task_always_eager": settings.celery_task_always_eager,
}

if settings.redis_url.startswith("rediss://"):
    celery_conf["broker_use_ssl"] = {"ssl_cert_reqs": ssl.CERT_NONE}
    celery_conf["redis_backend_use_ssl"] = {"ssl_cert_reqs": ssl.CERT_NONE}

celery.conf.update(**celery_conf)
