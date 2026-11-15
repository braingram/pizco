# -*- coding: utf-8 -*-
"""
    pyzco.util
    ~~~~~~~~~~

    Useful functions.

    :copyright: 2013 by Hernan E. Grecco, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import inspect


class SignalError(Exception):
    pass


class Signal(object):
    """PyQt like signal object
    """
    def __init__(self, nargs=0, kwargs=None, varargs=False, varkwargs=False):
        # add dummy types for signals or hide a pyqtSignal behind to resync
        # with qt main loop
        self.slots = []
        self._nargs = nargs
        if kwargs is None:
            self._kwargs = []
        else:
            self._kwargs = kwargs
        self._varargs = varargs
        self._varkwargs = varkwargs

    def connect(self, slot):
        # add dummy connection type maybe this the place to create the
        # pyqtSignals to be able to resync with qt event loop
        if slot not in self.slots:
            self.slots.append(slot)

    def disconnect(self, slot=None):
        if slot is None:
            self.slots = []
        else:
            self.slots.remove(slot)

    def _verify_emit(self, args, kwargs):
        if not self._varargs:  # check args
            if len(args) != self._nargs:
                raise SignalError(
                    "emit called with invalid number of args {}".format(
                        len(args)))
        if not self._varkwargs:  # check kwargs
            for k in kwargs:
                if k not in self._kwargs:
                    raise SignalError(
                        "emit called with invalid kwarg {}".format(
                            k))

    def emit(self, *args, **kwargs):
        # thread safety in qt main loop maybe pyqtSignals should be
        # called behind
        self._verify_emit(args, kwargs)
        for slot in self.slots:
            slot(*args, **kwargs)


def bind(sock, endpoint='tcp://127.0.0.1:0'):
    """Bind socket to endpoint accepting a variety of endpoint formats.

    If connection is tcp and port is 0 or not given, it will call bind_to_random_port.

    :param sock: Socket to bind
    :type sock: zmq.Socket
    :param endpoint: endpoint to bind as string or (address, port) tuple
    :type endpoint: tuple or str

    :return: bound endpoint
    :rtype: str
    """
    if not endpoint:
        endpoint = 'tcp://127.0.0.1:0'
    elif isinstance(endpoint, (tuple, list)):
        endpoint = 'tcp://{}:{}'.format(*endpoint)

    if endpoint.startswith('tcp://') and endpoint.endswith(':0'):
        endpoint = endpoint[:-2]
        port = sock.bind_to_random_port(endpoint)
        endpoint += ':' + str(port)
    else:
        sock.bind(endpoint)

    return endpoint
