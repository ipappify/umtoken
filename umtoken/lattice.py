# Path: umtoken/lattice.py

import math

def log_sum_exp(a, b):
    if a == float("-inf"):
        return b
    if b == float("-inf"):
        return a
    if a > b:
        return a + math.log1p(math.exp(b - a))
    else:
        return b + math.log1p(math.exp(a - b))

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
        logits_forward = self.logits_forward
        best_forward = self.best_forward
        edges = self.edges
        edges_start = self.edges_start
        neg_inf = float("-inf")
        for l in range(self.count-1):
            lf_left = logits_forward[l]
            if lf_left == neg_inf:
                continue
            for k in edges_start[l]:
                _, j, logit, _ = edges[k]
                new = lf_left + logit
                if new > logits_forward[j]:
                    logits_forward[j] = new
                    best_forward[j] = k
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
        logits_forward = self.logits_forward
        edges = self.edges
        edges_start = self.edges_start
        neg_inf = float("-inf")
        for l in range(self.count-1):
            lf_left = logits_forward[l]
            if lf_left == neg_inf:
                continue
            for k in edges_start[l]:
                _, j, logit, _ = edges[k]
                logits_forward[j] = log_sum_exp(logits_forward[j], lf_left + logit)
        self.forward_type = "sum"

    def backward_sum(self):
        logits_backward = self.logits_backward
        edges = self.edges
        edges_end = self.edges_end
        neg_inf = float("-inf")
        for l in reversed(range(self.count-1)):
            lb_right = logits_backward[l+1]
            if lb_right == neg_inf:
                continue
            for k in edges_end[l]:
                i, _, logit, _ = edges[k]
                logits_backward[i] = log_sum_exp(logits_backward[i], lb_right + logit)
        self.backward_type = "sum"

    def marginal_logits(self):
        assert self.forward_type == "sum"
        assert self.backward_type == "sum"

        lf = self.logits_forward
        lb = self.logits_backward
        edges = self.edges
        isfinite = math.isfinite
        neg_inf = float("-inf")
        logit_word = lf[-1]
        logits = [None] * len(edges)
        for k, e in enumerate(edges):
            i, j, logit, _ = e
            logit_i = lf[i]
            logit_j = lb[j]
            # P(eij|word) = P_fwd(i) * P(eij) * P_bwd(j) / P(word)
            if isfinite(logit_i) and isfinite(logit_j):
                logits[k] = logit + logit_i + logit_j - logit_word
            else:
                logits[k] = neg_inf

        return logits

    def removal_losses(self):
        assert self.forward_type == "sum"
        assert self.backward_type == "sum"

        # losses are negative logs of relative reductions of the word probability when a certain edge is removed
        lf = self.logits_forward
        lb = self.logits_backward
        edges = self.edges
        isfinite = math.isfinite
        exp = math.exp
        log = math.log
        logit_word = lf[-1]
        prob_word = exp(logit_word)
        prob_floor = 1e-20 * prob_word
        max_loss = log(1e+20)

        losses = [0.0] * len(edges)
        for k, e in enumerate(edges):
            i, j, logit, _ = e
            logit_i = lf[i]
            logit_j = lb[j]
            if not isfinite(logit_i) or not isfinite(logit_j):
                continue

            # L = -log[(P(word) - P(word w/o eij)) / P(word)]
            # TODO: there is probably a more numerically stable way to compute this
            prob_word_removed = prob_word - exp(logit + logit_i + logit_j)
            if prob_word_removed <= prob_floor:
                losses[k] = max_loss
            else:
                losses[k] = logit_word - log(prob_word_removed)

        return losses