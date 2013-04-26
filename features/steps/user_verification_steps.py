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

from etiktak.util import security
from etiktak.model.clients import models as clients

from features import api_handler

from lettuce import step
from lettuce import world

@step(u'Then I can verify the user')
def then_i_can_verify_the_user(step):
    world.client_uid = api_handler.verify_user(world.mobile_number, world.password, world.sms_challenge, world.client_challenge)

@step(u'Then I cannot verify the user with incorrect SMS challenge')
def then_i_cannot_verify_the_user_with_incorrect_challenge(step):
    try:
        api_handler.verify_user(world.mobile_number, world.password, "VERY UNLIKELY CHALLENGE", world.client_challenge)
        raise BaseException("Was able to verify client with incorrect challenge")
    except api_handler.WebserviceException:
        pass

@step(u'Then I cannot verify the user with incorrect client challenge')
def then_i_cannot_verify_the_user_with_incorrect_challenge(step):
    try:
        api_handler.verify_user(world.mobile_number, world.password, world.sms_challenge, "VERY UNLIKELY CHALLENGE")
        raise BaseException("Was able to verify client with incorrect challenge")
    except api_handler.WebserviceException:
        pass

@step(u'And I check that a challenge has been created in the database')
def and_I_check_that_a_challenge_has_been_created_in_the_database(step):
    verification = clients.SmsVerification.objects.get(world.mobile_number)
    # Override challenge with custom challenge
    world.sms_challenge = security.SMS.generate_sms_challenge()
    verification.sms_challenge_hash = security.hash(world.sms_challenge)
    verification.save()
