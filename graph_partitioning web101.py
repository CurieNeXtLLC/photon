# Copyright 2019 D-Wave Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ------- April 18 2021 -------
# Clone the graph partitioning example to reproduce the example in Quantum Programming 101
# curienext

# ------ Import necessary packages ----
import networkx as nx
from collections import defaultdict
from itertools import combinations
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import math

# ------- Set tunable parameters -------
num_reads = 50
gamma = 4

# ------- Set up our graph -------
G = nx.Graph()
G.add_edges_from([(0,4),(0,5),(1,2),(1,6), (2,4), (3,7), (5,6), (6,7)])

print("Graph on {} nodes created with {} out of {} possible edges.".format(len(G.nodes), len(G.edges), len(G.nodes) * (len(G.nodes)-1) / 2))

# ------- Set up our QUBO dictionary -------

# Initialize our Q matrix
Q = defaultdict(int)

# Contraint
lagrange = 4
for i in range(8):
    Q[(i,i)] += -7*lagrange
    for j in range(i+1,8):
        Q[(i,j)] +=2*lagrange

# Objective
for i, j in G.edges:
    Q[(i, i)] += 1
    Q[(j, j)] += 1
    Q[(i, j)] += -2

# Run the QUBO on the solver from your config file
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q,
                               num_reads=num_reads,
                               chain_strength=10,
                               label='Example - QC101')

# See if the best solution found is feasible, and if so print the number of cut edges.
sample = response.record.sample[0]

print(response)
