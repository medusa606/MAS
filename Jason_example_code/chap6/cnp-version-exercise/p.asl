// gets the price for the product,
// (a random value between 100 and 110).
price(Service,X) :- .random(R) & X = (10*R)+100.

plays(initiator,c). 

/* Plans */

// send a message to initiator introducing myself
// as a participant
+plays(initiator,In)
   :  .my_name(Me)
   <- .send(In,tell,introduction(participant,Me)).

+?cfp(CNPId,Task,Offer)
   :  price(Task,Offer)
   <- +proposal(CNPId,Task,Offer). // remember my proposal

@r1 +accept_proposal(CNPId)
   :  proposal(CNPId,Task,Offer)
   <- .print("My proposal '",Offer,"' won CNP ",CNPId,
             " for ",Task,"!").
      // build and deliver the product!
	  
@r2 +reject_proposal(CNPId)
   <- .print("I lost CNP ",CNPId, ".");
      -proposal(CNPId,_,_). // clean memory
	  
