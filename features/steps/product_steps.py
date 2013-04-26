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

from etiktak.model.products import models as products

from features import api_handler

from lettuce import step
from lettuce import world

import random

@step(u'And I can contribute to the crowd database on an existing product')
def and_i_can_contribute_to_crowd_database_on_an_existing_product(step):
    product = create_random_product()
    api_handler.create_product_location(world.mobile_number, world.password, world.client_uid, product.barcode, products.BARCODE_TYPES.EAN13, "1.0, 2.0")

@step(u'Then I cannot contribute to the crowd database on an existing product')
def then_i_cannot_contribute_to_the_crowd_database_on_an_existing_product(step):
    product = create_random_product()
    try:
        api_handler.create_product_location(world.mobile_number, world.password, world.client_uid, product.barcode, products.BARCODE_TYPES.EAN13, "1.0, 2.0")
        raise BaseException("Was able to contribute even though not verified")
    except api_handler.WebserviceException:
        pass

@step(u'I cannot contribute to the crowd database on an existing product with non-existant user')
def i_cannot_contribute_to_the_crowd_database_on_an_existing_product_with_non_existant_user(step):
    world.mobile_number = "I_DONT_EXIST"
    world.client_uid = "UID_THAT_DOESNT_EXIST"
    product = create_random_product()
    try:
        api_handler.create_product_location(world.mobile_number, world.password, world.client_uid, product.barcode, products.BARCODE_TYPES.EAN13, "1.0, 2.0")
        raise BaseException("Was able to contribute even though I don't exist!")
    except api_handler.WebserviceException:
        pass



def create_random_product():
    product_barcode = "test_barcode_%f" % random.random()
    category = products.ProductCategory.create_product_category("test_category_%f" % random.random())
    return products.Product.create_product("test_product_%f" % random.random(), product_barcode, products.BARCODE_TYPES.EAN13, category)
