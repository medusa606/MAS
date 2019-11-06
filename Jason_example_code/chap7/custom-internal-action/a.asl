/* Initial goals */

!start.
!test(4).
!test(33).
!test(a).

/* Plans */

// use math.odd with backtrack
+!start : math.odd(X) & X > 20 <- .print(X," is the first odd number after 20.").

// use math.odd with a ground argument
+!test(a) : math.odd(3) <- .print("3 is odd.").
+!test(X) : math.odd(X) <- .print(X," is odd.").
+!test(X) : true        <- .print(X," is not odd.").
