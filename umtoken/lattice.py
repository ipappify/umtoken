# Path: umtoken/lattice.py

import math

import numpy as np

def log_sum_exp(a, b):
    if a == float("-inf"):
        return b
    if b == float("-inf"):
        return a
    if a > b:
        return a + np.log1p(np.exp(b - a))
    else:
        return b + np.log1p(np.exp(a - b))

class Lattice():
    def __init__(self, count):
        assert count > 1
        self.count = count
        self.edges = []
        self.edges_start = [[] for _ in range(count-1)]
        self.edges_end = [[] for _ in range(count-1)]
        self.reset_logits()

    def reset_logits(self):
        self.logits_forward = [float("-inf")] * self.count
        self.logits_forward[0] = 0.0
        self.best_forward = [None] * self.count
        self.logits_backward = [float("-inf")] * self.count
        self.logits_backward[-1] = 0.0
        self.forward_type = None
        self.backward_type = None

    def add_edge(self, start, end, logit, data):
        self.edges.append((start, end, logit, data))
        self.edges_start[start].append(len(self.edges)-1)
        self.edges_end[end-1].append(len(self.edges)-1)

    def forward_max(self):
        for l in range(self.count-1):
            for k in self.edges_start[l]:
                i, j, logit, _ = self.edges[k]
                if self.logits_forward[i] + logit > self.logits_forward[j]:
                    self.logits_forward[j] = self.logits_forward[i] + logit
                    self.best_forward[j] = k
        self.forward_type = "max"

    def backtrack(self):
        assert self.forward_type == "max"
        if self.best_forward[-1] is None:
            return None
        result = []
        i = self.count - 1
        while i > 0:
            i, j, logit, data = self.edges[self.best_forward[i]]
            result.append((i, j, logit, data))
        return result[::-1]
    
    def viterbi(self):
        if self.forward_type != "max":
            if self.forward_type is not None:
                self.reset_logits()
            self.forward_max()
        return self.backtrack()

    def forward_sum(self):
        for l in range(self.count-1):
            for k in self.edges_start[l]:
                i, j, logit, _ = self.edges[k]
                self.logits_forward[j] = log_sum_exp(self.logits_forward[j], self.logits_forward[i] + logit)
        self.forward_type = "sum"

    def backward_sum(self):
        for l in reversed(range(self.count-1)):
            for k in self.edges_end[l]:
                i, j, logit, _ = self.edges[k]
                self.logits_backward[i] = log_sum_exp(self.logits_backward[i], self.logits_backward[j] + logit)
        self.backward_type = "sum"

    def marginal_logits(self):
        assert self.forward_type == "sum"
        assert self.backward_type == "sum"

        logit_word = self.logits_forward[-1]
        logits = [None] * len(self.edges)
        for k, e in enumerate(self.edges):
            i, j, logit, _ = e
            logit_i = self.logits_forward[i]
            logit_j = self.logits_backward[j]
            # P(eij|word) = P_fwd(i) * P(eij) * P_bwd(j) / P(word)
            if math.isfinite(logit_i) and math.isfinite(logit_j):
                logits[k] = logit + logit_i + logit_j - logit_word
            else:
                logits[k] = float("-inf")

        return logits
    
    def removal_losses(self):
        assert self.forward_type == "sum"
        assert self.backward_type == "sum"

        # losses are negative logs of relative reductions of the word probability when a certain edge is removed
        logit_word = self.logits_forward[-1]
        prob_word = np.exp(logit_word)

        losses = [0.0] * len(self.edges)
        for k, e in enumerate(self.edges):
            i, j, logit, _ = e
            logit_i = self.logits_forward[i]
            logit_j = self.logits_backward[j]
            if not math.isfinite(logit_i) or not math.isfinite(logit_j):
                continue

            # L = -log[(P(word) - P(word w/o eij)) / P(word)]
            # TODO: there is probably a more numerically stable way to compute this
            prob_word_removed = prob_word - np.exp(logit + logit_i + logit_j)
            if prob_word_removed <= 1e-20 * prob_word:
                losses[k] = np.log(1e+20)
            else:
                losses[k] = logit_word - np.log(prob_word_removed)

        return losses