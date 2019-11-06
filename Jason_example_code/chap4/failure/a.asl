!g1. // initial goal

@p1 +!g1    : true <- !g2(X); .print("end g1 ",X).
@p2 +!g2(X) : true <- !g3(X); .print("end g2 ",X).
@p3 +!g3(X) : true <- !g4(X); .print("end g3 ",X).
@p4 +!g4(X) : true <- !g5(X); .print("end g4 ",X).
@p5 +!g5(_) : true <- .fail.

@f1 -!g3(failure) : true <- .print("in g3 failure").
