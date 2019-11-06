// Agent a in project sel_rel.mas2j

/* Initial beliefs and rules */

a(10).
a(5).
b(20).

/* Initial goals */

!start.

/* Plans */

+!start : true <- +g(10,5)[source(ag1)].

@p1 +g(X,Y) : true <- .print(p1) . 
@p2 +g(X,Y) : a(Y) & not b(X) <- .print(p2). 
@p3 +g(X,_) : a(Y) & Y > X <- .print(p3) . 
@p4 +g(X,Y)[source(self)] : true <- .print(p4) . 
@p5 +g(X,Y)[source(self),source(ag1)] : true <- .print(p5) . 
@p6[all_unifs] +g(10,Y) : a(Y) <- .print(p6). 
