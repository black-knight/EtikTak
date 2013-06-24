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

import random

from features import api_handler
from features.steps import user_steps
from features.steps import sms_steps
from features.steps import user_verification_steps
from features.steps import product_steps

from etiktak.util import clustering
from etiktak.util import util
from etiktak.model.products import models as products
from etiktak.model.stores import models as stores

from lettuce import step
from lettuce import world

@step(u'Given I simulate that a user scans "([^"]*)" times in a radius of "([^"]*)" meters')
def given_i_simulate_that_a_user_scans_group1_times_in_a_radius_of_group2_meters(step, group1, group2):
    user_steps.given_i_apply_for_a_new_user_with_mobile_number_group1_and_password_group2(None, "40000000", "Test1234")
    user_verification_steps.and_I_check_that_a_challenge_has_been_created_in_the_database(None)
    sms_steps.and_i_simulate_that_an_sms_has_been_successfully_sent(None)
    user_verification_steps.then_i_can_verify_the_user(None)
    create_random_product_scans(latitude_center=56.08, longitude_center=10.11, radius=float(group2), count=int(group1))

@step(u'And I run the clustering algorithm')
def and_i_run_the_clustering_algorithm(step):
    world.clustering_alg = clustering.Clustering()
    world.clustering_alg.start()

@step(u'Then the product scans have been clustered correctly')
def then_the_product_scans_have_been_clustered_correctly(step):
    world.clustering_alg.verify_cluster_correctness()



def create_random_product_scans(latitude_center, longitude_center, radius, count):
    store = stores.Store.create_store("test_store_%f" % random.random())
    stores.StoreInstance.create_store_instance("test_address_%f" % random.random(), latitude_center, longitude_center, store)
    product = product_steps.create_random_product()
    for i in range(1, count):
        latitude = latitude_center + (random.random() * util.meters_to_latitude(radius))
        longitude = longitude_center + (random.random() * util.meters_to_longitude(radius, latitude))
        api_handler.create_product_scan(world.mobile_number, world.password, world.client_uid, product.barcode, products.BARCODE_TYPES.EAN13, str(latitude), str(longitude))
