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
            neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(node)
            if len(neighborhood) == 0:
                self.handle_noise(node)
            elif len(neighborhood) < products.NEIGHBORHOOD_MIN_DENSITY:
                self.handle_edge_point(node, neighborhood)
            else:
                self.handle_density_point(node, neighborhood)
            node.save()

    def emit_node(self):
        """
         Emits an unhandled node, that is, a node that is marked as NOT_VISITED.
        """
        return products.ProductScanClusterNode.objects.get_next_node()

    def handle_noise(self, node):
        """
         Noise points are points with no neighbors, and thus they belong to no cluster.
        """
        node.status = products.CLUSTER_NODE_STATUS.NOISE
        node.cluster_number = -1

    def handle_edge_point(self, node, neighborhood):
        """
         Edge points are points that are not themself density points, but lies in the neighborhood of
         a density point, and so they are assigned a random neighborhood cluster.
        """
        for neighborhood_node in neighborhood:
            other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(neighborhood_node)
            if len(other_neighborhood) >= products.NEIGHBORHOOD_MIN_DENSITY:  # Density node - should be in cluster, so choose this cluster
                if neighborhood_node.cluster_number == -1:
                    self.form_new_cluster(neighborhood_node, other_neighborhood)
                    neighborhood_node.save()
                node.cluster_number = neighborhood_node.cluster_number
                return

    def handle_density_point(self, node, neighborhood):
        """
         Density points themself form a cluster, so all neighborhood density points should be in the
         same cluster as this. If two neighborhood clusters are detected, they are merged. Edge points
         are merged into the cluster as well, though they might belong to another cluster as an edge
         point already.
        """
        if not self.any_neighborhood_node_is_in_cluster(neighborhood):
            self.form_new_cluster(node, neighborhood)  # None of neighborhoods nodes are in clusters, so form a new cluster
            return
        node.cluster_number = -1
        edge_nodes_to_include_in_same_cluster = []
        density_nodes_to_include_in_same_cluster = []
        for neighborhood_node in neighborhood:
            other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(neighborhood_node)
            if len(other_neighborhood) >= products.NEIGHBORHOOD_MIN_DENSITY:  # Density node - should be in cluster
                if neighborhood_node.cluster_number == -1:
                    density_nodes_to_include_in_same_cluster.append(neighborhood_node)
                    density_nodes_to_include_in_same_cluster = density_nodes_to_include_in_same_cluster + other_neighborhood
                elif node.cluster_number == -1:  # First visited cluster - choose as node's cluster
                    node.cluster_number = neighborhood_node.cluster_number
                else:  # Other cluster - since node is a density node it should be in all neighborhood clusters that are also density nodes
                    #self.merge_clusters(node.cluster_number, neighborhood_node.cluster_number)
                    pass
            else:
                edge_nodes_to_include_in_same_cluster.append(neighborhood_node)
        print "%i" % node.cluster_number
        print edge_nodes_to_include_in_same_cluster
        self.include_nodes_in_cluster(edge_nodes_to_include_in_same_cluster, node.cluster_number)  # Include edge nodes in this cluster as well
        self.include_nodes_in_cluster(density_nodes_to_include_in_same_cluster, node.cluster_number)  # Include edge nodes in this cluster as well

    def include_nodes_in_cluster(self, nodes, cluster_number):
        for node in nodes:
            node.cluster_number = cluster_number
            node.save()

    def merge_clusters(self, dest_cluster_number, other_cluster_number):
        nodes = products.ProductScanClusterNode.objects.get_nodes_in_cluster(other_cluster_number)
        for node in nodes:
            node.cluster_number = dest_cluster_number
            node.save()

    def any_neighborhood_node_is_in_cluster(self, neighborhood):
        for neighborhood_node in neighborhood:
            if neighborhood_node.cluster_number is not -1:
                return True
        return False

    def form_new_cluster(self, node, neighborhood):
        node.cluster_number = products.ProductScanClusterNode.objects.get_next_cluster_number()
        node.status = products.CLUSTER_NODE_STATUS.VISITED
        for neighborhood_node in neighborhood:
            neighborhood_node.cluster_number = node.cluster_number
            neighborhood_node.status = products.CLUSTER_NODE_STATUS.VISITED
            neighborhood_node.save()



    def verify_cluster_correctness(self):
        print "Verifying cluster correctness...\n"
        all_nodes = list(products.ProductScanClusterNode.objects.all())
        while len(all_nodes) > 0:
            node = all_nodes[0]
            all_nodes.pop(0)
            self.verify_node_correctness(node, all_nodes)

    def verify_node_correctness(self, node, all_nodes):
        neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(node)
        if len(neighborhood) == 0:
            assert node.status == products.CLUSTER_NODE_STATUS.NOISE, "Expected node to be NOISE (has 0 neighbors), but found it to be: " % node.status
        elif len(neighborhood) < products.NEIGHBORHOOD_MIN_DENSITY:
            self.verify_edge_node(node, neighborhood)
        else:
            self.verify_density_node_neighborhood(node, neighborhood, all_nodes)

    def verify_edge_node(self, node, neighborhood):
        if node.cluster_number != -1:
            print
            print "-----"
            for neighborhood_node in neighborhood:
                if neighborhood_node.cluster_number == node.cluster_number:
                    other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(neighborhood_node)
                    print len(other_neighborhood)
                    if len(other_neighborhood) >= products.NEIGHBORHOOD_MIN_DENSITY:
                        return
            print
            assert False, "Expected one density neighbor node of clustered edge node in same cluster"
        else:
            for neighborhood_node in neighborhood:
                other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(neighborhood_node)
                assert len(other_neighborhood) < products.NEIGHBORHOOD_MIN_DENSITY, "Expected all neighbors of non-clustered nodes to be non-clustered as well, but found neighborhood node with density %i (versus self node density %i)" % (len(other_neighborhood), len(neighborhood))

    def verify_density_node_neighborhood(self, node, neighborhood, all_nodes):
        return
        while len(neighborhood) > 0:
            other_node = neighborhood[0]
            neighborhood.pop(0)
            if other_node in all_nodes:
                all_nodes.remove(other_node)
            other_neighborhood = products.ProductScanClusterNode.objects.get_neighborhood_nodes(other_node)
            if len(other_neighborhood) >= products.NEIGHBORHOOD_MIN_DENSITY:
                assert node.status == other_node.status, "Expected density nodes to have same status as all of its neighbor density nodes (%i versus %i)" % (node.status, other_node.status)
                assert node.cluster_number == other_node.cluster_number, "Expected density node to be in same cluster as all of its neighbor density nodes"
                neighborhood = neighborhood + other_neighborhood
