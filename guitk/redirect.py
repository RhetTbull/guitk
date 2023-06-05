"""Redirect stdout/stderr """

from __future__ import annotations

import sys


class _StdOutRedirectBaseClass:
    """Base class for StdOutRedirect and StdErrRedirect"""

    def __init__(self):
        self._echo = False
        self._listeners = {}
        self._listener_count = 0
        self._redirect = False

        self.stdout = False
        self.stderr = False

    @property
    def echo(self):
        return self._echo

    @echo.setter
    def echo(self, val):
        self._echo = val

    def register(self, listener):
        if not callable(listener):
            raise ValueError("listener must be callable")
        self._listener_count += 1
        listener_id = self._listener_count
        self._listeners[listener_id] = listener
        self.enable_redirect()
        return listener_id

    def deregister(self, listener_id):
        del self._listeners[listener_id]
        if not self._listeners:
            self.disable_redirect()

    def write(self, line):
        if self._redirect:
            for listener in self._listeners:
                self._listeners[listener](line)
            if self.echo:
                if self.stdout:
                    sys.__stdout__.write(line)
                if self.stderr:
                    sys.__stderr__.write(line)

    def flush(self):
        pass

    def disable_redirect(self):
        self._redirect = False
        if self.stdout:
            sys.stdout = sys.__stdout__
        if self.stderr:
            sys.stderr = sys.__stderr__

    def enable_redirect(self):
        self._redirect = True
        if self.stdout:
            sys.stdout = self
        if self.stderr:
            sys.stderr = self

    def __del__(self):
        if self.stdout:
            sys.stdout = sys.__stdout__
        if self.stderr:
            sys.stderr = sys.__stderr__


class StdOutRedirect(_StdOutRedirectBaseClass):
    """Singleton class that handles redirect"""

    def __new__(cls, *args, **kwargs):
        """create new object or return instance of already created singleton"""
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        if hasattr(self, "_init"):
            return
        super().__init__()
        self._init = True
        self.stdout = True


class StdErrRedirect(_StdOutRedirectBaseClass):
    """Singleton class that handles redirect"""

    def __new__(cls, *args, **kwargs):
        """create new object or return instance of already created singleton"""
        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self):
        if hasattr(self, "_init"):
            return
        super().__init__()
        self._init = True
        self.stderr = True
