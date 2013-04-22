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

from features import api_handler

from lettuce import step
from lettuce import world

@step(u'Given I apply for a new user with mobile number "([^"]*)" and password "([^"]*)"')
def given_i_apply_for_a_new_user_with_mobile_number_group1_and_password_group2(step, group1, group2):
    world.mobile_number = group1
    world.password = group2
    world.client_uid= None
    api_handler.apply_for_user_with_password(world.mobile_number, world.password)

@step(u'Given I apply for a new user with mobile number "([^"]*)" and UID "([^"]*)"')
def given_i_apply_for_a_new_user_with_mobile_number_group1_and_uid_group2(step, group1, group2):
    world.mobile_number = group1
    world.password = None
    world.client_uid = group2
    api_handler.apply_for_user_with_uid(world.mobile_number, world.client_uid)

@step(u'Given there is already a user with mobile number "([^"]*)"')
def given_there_is_already_a_user_with_mobile_number_group1(step, group1):
    world.mobile_number = group1
    api_handler.apply_for_user_with_password(world.mobile_number, "test1234")

@step(u'Then I cannot apply for a new user with that mobile number')
def then_i_cannot_apply_for_a_new_user_with_that_mobile_number(step):
    try:
        api_handler.apply_for_user_with_password(world.mobile_number, "not_test1234")
    except BaseException:
        return
    raise BaseException("I was able to apply from mobile phone number already used: %s" % world.mobile_number)
