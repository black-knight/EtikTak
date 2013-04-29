# encoding: utf-8

# Copyright (c) 2012, Daniel Andersen (dani_ande@yahoo.dk)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import inspect

class Choice(object):
    """
    A class that turns field members into a list of tuples for use in Django models choices.

    Examples:
    >>> class UserLevels(Choice):
        USER = (u'USER', u'User')
        MODERATOR = (u'MODERATOR')
        ADMIN = (u'ADMIN', u'God')
    >>> list(UserLevels)
    [(u'ADMIN', u'God'), (u'MODERATOR', u'MODERATOR'), (u'USER', u'User')]
    >>> UserLevels.ADMIN
    u'ADMIN'
    """
    class __metaclass__(type):
        def __init__(cls, name, type, other):
            cls._data = []
            for name, value in inspect.getmembers(cls):
                if not name.startswith("_") and not inspect.isfunction(value):
                    if isinstance(value,tuple) and len(value) > 1:
                        data = value
                    else:
                        data = (value, " ".join([x.capitalize() for x in name.split("_")]),)
                    cls._data.append(data)
                    setattr(cls, name, data[0])

        def __iter__(cls):
            for value, data in cls._data:
                yield value, data
