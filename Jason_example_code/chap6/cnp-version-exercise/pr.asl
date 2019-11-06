// belief to be used to answer a CFP
cfp(CNPId,Task,refuse).

plays(initiator,c). 
+plays(initiator,In)
   :  .my_name(Me)
   <- .send(In,tell,introduction(participant,Me)).


