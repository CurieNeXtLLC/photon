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

# ------- May 23 2021 -------
# Clone the graph partitioning example to reproduce the example in "Quantum Computing Tutorials Part 2: QUBOs and Embedding"
# Problem: Pick the pair of boxes with the smallest sum
# curienext

# ------ Import necessary packages ----
import networkx as nx
from collections import defaultdict
from itertools import combinations
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
import math

# ------- Set tunable parameters -------
num_reads = 400
chain_strth = 10
lagrange = 40
qsize = 3

# ------- Set up our QUBO dictionary -------

# Initialize our Q matrix
Q = defaultdict(int)

# Contraint

for i in range(qsize):
    Q[(i,i)] += -3*lagrange
    for j in range(i+1,qsize):
        Q[(i,j)] +=2*lagrange

#print (Q)

# Objective
# pick the pair of boxes with the smallest sum:
Q[(0, 0)] += 17
Q[(1, 1)] += 21
Q[(2, 2)] += 19

#print (Q)

# Run the QUBO on the solver from your config file
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample_qubo(Q,
                               num_reads=num_reads,
                               chain_strength=chain_strth,
                               label='Tutorial2-pick two smallest')

# See if the best solution found is feasible, and if so print the number of cut edges.
sample = response.record.sample[0]

print(response)
