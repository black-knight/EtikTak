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

# tests.py
import sys, EtikTakProject.settings, re, os, doctest, unittest, imp

# import your base Django project
import EtikTakApp

# Django already runs these, don't include them again
ALREADY_RUN = ['tests.py', 'models.py', '__init__.py']

def find_untested_modules(package):
    dirindex = len(os.getcwd()) + len("/")
    """ Gets all modules not already included in Django's test suite """
    files = [re.sub('\.py$', '', os.path.join(root, f)[dirindex:])
             for root, dirnames, filenames in os.walk(os.path.dirname(package.__file__))
             for f in filenames if f.endswith(".py") and os.path.basename(f) not in ALREADY_RUN]
    return [imp.load_module(file, *imp.find_module(os.path.basename(file), [file[:len(file) - len(os.path.basename(file)) - 1]]))
            for file in files]

def modules_callables(module):
    return [m for m in dir(module) if callable(getattr(module, m))]

def has_doctest(docstring):
    return ">>>" in docstring

__test__ = {}
for module in find_untested_modules(EtikTakApp):
    print "Module: %s" % module.__name__
    for method in modules_callables(module):
        docstring = str(getattr(module, method).__doc__)
        if has_doctest(docstring):

            print "Found doctest(s) " + module.__name__ + "." + method

            # import the method itself, so doctest can find it
            _temp = __import__(module.__name__, globals(), locals(), [method])
            locals()[method] = getattr(_temp, method)

            # Django looks in __test__ for doctests to run
            __test__[method] = getattr(module, method)
