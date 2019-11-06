sum(0).
+vl(1) : sum(S) <- .print(S+1). // the last tell from sender
@u[atomic] +vl(X) : sum(S) <- NS = S + 1; -+sum(NS).
