/* Initial goals */

!startCNP(1,fix(computer)).

/* Plans */


+!startCNP(Id,Task) 
   <- .wait(2000);  // wait for participants' introduction
      .findall(Name,introduction(participant,Name),LP);
      .print("Sending CFP to ",LP);
      !ask_proposal(Id,Task,LP).

/** ask proposals from all agents in the list */

// all participants have been asked, proceed with contract
+!ask_proposal(CNPId,_,[])
   <- !contract(CNPId). 

// there is a participant to ask
+!ask_proposal(CNPId,Task,[Ag|T])
   <- .send(Ag,
            askOne,
            cfp(Id,Task,Offer),
            Answer, 
            2000); // timeout = 2 seconds
      !add_proposal(Ag,Answer); // remember this proposal
      !ask_proposal(CNPId,Task,T).

+!add_proposal(Ag,cfp(Id,_,Offer))
   <- +offer(Id,Offer,Ag).  // remember Ag's offer
+!add_proposal(_,timeout).  // timeout, do nothing
+!add_proposal(_,false).    // answer is false, do nothing
   
+!contract(CNPId) : true
   <- .findall(offer(O,A),offer(CNPId,O,A),L);
      .print("Offers are ",L);
      L \== [];
      .min(L,offer(WOf,WAg));
      .print("Winner is ",WAg," with ",WOf);
      !announce_result(CNPId,L,WAg).

+!announce_result(_,[],_).
// announce to the winner
+!announce_result(CNPId,[offer(O,WAg)|T],WAg) 
   <- .send(WAg,tell,accept_proposal(CNPId));
      !announce_result(CNPId,T,WAg).
// announce to others
+!announce_result(CNPId,[offer(O,LAg)|T],WAg) 
   <- .send(LAg,tell,reject_proposal(CNPId));
      !announce_result(CNPId,T,WAg).
	  
