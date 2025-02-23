from typing import List, Tuple
import pytest

from synthora.workflows import task, BaseTask, BaseScheduler, ThreadPoolScheduler, ProcessPoolScheduler, AsyncTask, BasicContext, MultiProcessContext

def add(ctx: BasicContext, a: int, b: int) -> int:
    print(f"Adding {a} and {b}")
    with ctx:
        ctx['log'] = [a + b] if 'log' not in ctx else ctx['log'] + [
            a + b
        ]
    return a + b



class TestContexts:
    def test_basiccontext(self):
        flow = BaseTask(add).si(1, 2) >> BaseTask(add).s(3)
        flow.run()
        assert flow.context['log'] == [3, 6]

        flow = ThreadPoolScheduler() >> BaseTask(add).si(1, 2) >> BaseTask(add).s(3)
        flow.run()
        assert flow.context['log'] == [3, 6]
    
    def test_multiprocesscontext(self):
        flow = ProcessPoolScheduler() >> BaseTask(add).si(1, 2) >> BaseTask(add).s(3)
        flow.run()
        assert flow.context['log'] == [3, 6]
    
    
    
    