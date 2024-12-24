from abc import ABC


class BaseTask(ABC):
    def __init__(self, func, immutable: bool = False, flat_result: bool = False):
        self.func = func
        self.immutable = immutable
        self.state = None
        self.meta_data = None
        self.on_error = None
        self._args = []
        self._kwargs = {}
        self._result = None
        self.flat_result = flat_result

    def result(self):
        return self._result

    def signature(self, args, kwargs, immutable=False, on_error=None):
        self._args = list(args)
        self._kwargs = kwargs
        self.immutable = immutable
        self.on_error = on_error
        return self

    def s(self, *args, **kwargs):
        self._args = list(args)
        self._kwargs = kwargs
        return self

    def si(self, *args, **kwargs):
        self._args = list(args)
        self._kwargs = kwargs
        self.immutable = True
        return self

    def set_mutable(self, mutable: bool):
        self.immutable = mutable

    def __call__(self, *args, **kwargs):
        if self.immutable:
            self._result = self.func(*self._args, **self._kwargs)
            return self._result
        args += tuple(self._args)
        kwargs.update(self._kwargs)
        self._result = self.func(*args, **kwargs)
        return self._result


class AsyncTask(BaseTask):

    async def __call__(self, *args, **kwargs):
        if self.immutable:
            self._result = await self.func(*self._args, **self._kwargs)
            return self._result
        args += self._args
        kwargs.update(self._kwargs)
        self._result = await self.func(*args, **kwargs)
        return self._result
