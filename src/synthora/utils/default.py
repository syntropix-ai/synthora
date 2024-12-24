from synthora.workflows.scheduler.base import BaseScheduler
from synthora.workflows.scheduler.thread_pool import ThreadPoolScheduler

DEFAULT_CHAIN_SCHEDULER = BaseScheduler
DEFAULT_GROUP_SCHEDULER = ThreadPoolScheduler
