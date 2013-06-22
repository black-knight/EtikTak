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

class Clustering:
    def start(self):
        """
         Starts the clustering algorithm. All nodes that are marked NOT_VISITED will be visited
         and handled.
        """
        print "Clustering started!\n"
        while True:
            node = self.emit_node()
            if node is None:
                return
            self.handle_node(node)

    def emit_node(self):
        """
         Emits an unhandled node, that is, a node that is marked as NOT_VISITED.
        """
        return products.ProductScanClusterNode.objects.get_next_node()

    def approx_node(self, node):
        """
        Updates the clusters with a node. This is only done approximately; that is, when the
        full clustering algorithm has been run, the clusters might be updated.
        """
        neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(node=node, max_nodes=products.NEIGHBORHOOD_MIN_DENSITY)
        if len(neighborhood) == 0:
            self.handle_noise(node)
        else:
            self.approx_node_from_neighborhood(node, neighborhood)
        node.save()

    def approx_node_from_neighborhood(self, node, neighborhood):
        """
         Approximates a node's cluster based on its neighborhood. Any neighbor node that resides
         within a cluster can be choosen as cluster neighbor.
        """
        for neighborhood_node in neighborhood:
            if neighborhood_node.cluster_number is not -1:
                node.status = products.CLUSTER_NODE_STATUS.VISITED
                node.cluster_number = neighborhood_node.cluster_number
                return
        self.handle_noise(node)

    def handle_node(self, node):
        """
        Updates the clusters with this node.
        """
        node.status = products.CLUSTER_NODE_STATUS.VISITED
        neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(node)
        if len(neighborhood) < products.NEIGHBORHOOD_MIN_DENSITY:
            self.handle_noise(node)
        else:
            self.expand_cluster(node, neighborhood)
        node.save()

    def handle_noise(self, node):
        """
         Noise points are points with no neighbors, and thus they belong to no cluster.
        """
        node.status = products.CLUSTER_NODE_STATUS.NOISE
        node.cluster_number = -1

    def expand_cluster(self, node, neighborhood):
        """
         Density points themself form a cluster, so all neighborhood density points should be in the
         same cluster as this.
        """
        node.cluster_number = products.ProductScanClusterNode.objects.get_next_cluster_number()
        neighborhood_set = set(neighborhood)
        already_visited_set = set()
        while len(neighborhood_set) > 0:
            neighborhood_node = neighborhood_set.pop()
            already_visited_set.add(neighborhood_node)
            if neighborhood_node.status is not products.CLUSTER_NODE_STATUS.VISITED:
                neighborhood_node.status = products.CLUSTER_NODE_STATUS.VISITED
                neighborhood_node.save()
                other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(neighborhood_node)
                if len(other_neighborhood) >= products.NEIGHBORHOOD_MIN_DENSITY:
                    neighborhood_set |= set(other_neighborhood) - already_visited_set
            if neighborhood_node.cluster_number is -1:
                neighborhood_node.cluster_number = node.cluster_number
                neighborhood_node.save()



    def verify_cluster_correctness(self):
        print "Verifying cluster correctness...\n"
        all_nodes = list(products.ProductScanClusterNode.objects.all())
        for node in all_nodes:
            self.verify_node_correctness(node)

    def verify_node_correctness(self, node):
        neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(node)
        if len(neighborhood) == 0:
            assert node.status == products.CLUSTER_NODE_STATUS.NOISE, "Expected node to be NOISE (has 0 neighbors), but found it to be: " % node.status
        elif len(neighborhood) < products.NEIGHBORHOOD_MIN_DENSITY:
            self.verify_edge_node(node, neighborhood)
        else:
            self.verify_density_node_neighborhood(node, neighborhood)

    def verify_edge_node(self, node, neighborhood):
        if node.cluster_number != -1:
            for neighborhood_node in neighborhood:
                if neighborhood_node.cluster_number == node.cluster_number:
                    other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(neighborhood_node)
                    if len(other_neighborhood) >= products.NEIGHBORHOOD_MIN_DENSITY:
                        return
            assert False, "Expected one density neighbor node of clustered edge node in same cluster"
        else:
            for neighborhood_node in neighborhood:
                other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(neighborhood_node)
                assert len(other_neighborhood) < products.NEIGHBORHOOD_MIN_DENSITY, "Expected all neighbors of non-clustered nodes to be non-clustered as well, but found neighborhood node with density %i (versus self node density %i)" % (len(other_neighborhood), len(neighborhood))

    def verify_density_node_neighborhood(self, node, neighborhood):
        for other_node in neighborhood:
            other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(other_node)
            if len(other_neighborhood) >= products.NEIGHBORHOOD_MIN_DENSITY:
                assert node.status == other_node.status, "Expected density nodes to have same status as all of its neighbor density nodes (%i versus %i)" % (node.status, other_node.status)
                assert node.cluster_number == other_node.cluster_number, "Expected density node to be in same cluster as all of its neighbor density nodes"
