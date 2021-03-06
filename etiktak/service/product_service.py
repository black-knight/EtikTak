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

from etiktak.model.clients import models as clients
from etiktak.model.products import models as products
from etiktak.util.clustering import *


def create_product_scan(mobile_number, password, uid, barcode, barcode_type, scan_latitude, scan_longitude):
    client_by_password = clients.Client.objects.get_by_password(mobile_number, password)
    client_by_uid = clients.Client.objects.get_by_uid(uid)
    assert client_by_password.uid == client_by_uid.uid, "Incorrect credentials provided"
    product = products.Product.objects.get(barcode=barcode, barcode_type=barcode_type)
    scan = products.ProductScan.create_product_scan(product=product, scan_latitude=scan_latitude, scan_longitude=scan_longitude, client=client_by_uid)
    # print generate_feedback_from_scan(scan)
    return generate_feedback_from_scan(scan)


def generate_feedback_from_scan(scan):
    node = products.ProductScanClusterNode.objects.get_by_scan(scan)
    clustering_instance.approx_node(node)
    return {"store_certainty": calculate_store_certainty(node),
            "store": suggested_store(node)}


def calculate_store_certainty(node):
    if node.product_scan.store_instance is not None:
        return 0.75
    elif node.cluster_number is not -1:
        return 0.5
    else:
        return 0


def suggested_store(node):
    if node.product_scan.store_instance is not None:
        return node.product_scan.store_instance.store.name
    else:
        return ""
