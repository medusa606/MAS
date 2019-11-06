!count. // initial goal.

+!count : not count_exec(_) <- +count_exec(1); .print("first run"). 
+!count : count_exec(X)     <- -+count_exec(X+1); .print("run ",X," time(s)"). 

