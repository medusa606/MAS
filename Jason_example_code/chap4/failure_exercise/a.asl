// Agent a in project failure_exercise.mas2j

/* Initial beliefs and rules */

/* Initial goals */

!start.

/* Plans */

+!start : true <- +b.

+b <- !g1; a1.
+!g1 <- !g2.
+!g2 <- .fail; a4.

-!g1 : true <- a5.
