/* Initial goals */

!start(5).
!free(5).

/* Plans */

+!start(0).
+!start(X) <- .print(X); !start(X-1).

+!free(0).

@l[idle] // *** Add/Remove this annotation and notice the difference ***
+!free(X) <- .print(free); !free(X-1).
