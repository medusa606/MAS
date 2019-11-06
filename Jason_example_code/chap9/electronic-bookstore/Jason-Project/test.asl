// Agent test in project eletronicBookstore.mas2j

/* Initial beliefs and rules */

/* Initial goals */

!start.

/* Plans */

+!start
   <- .send(login,askOne,user_logon(jomi,"fred"),Ans);
      .print("Login = ",Ans);
      Ans \== false; // only continues if Ans was ok
      
      .send(jomi,askOne,book_suggestion,L);
      .print("Suggestions = ",L);
	  !show_books(L);

      .send(jomi,askOne,find_book("Dan",LFound1),find_book("Dan",LFound1));
      .print("Search result for Dan = ",LFound1);
	  !show_books(LFound1);
	  
      .send(jomi,askOne,find_book("Programming",_),find_book(_,LFound2));
      .print("Search result for Programming = ",LFound2);
	  !show_books(LFound2);
      
      //.send(jomi,askOne,delivery_options(4,2),Opts);
      //.print("Delivery options = ", Opts);
      
      // get the first option
      //Opts = delivery_confirm(_,_,delivery_options([option(OptId,_,_)|_]));
      //.send(jomi,tell,purchase(4,2,OptId));

      .wait(500);
      .send(stockManager,askOne,book(4,B4),book(4,B4[stock(B4Stock)]));
      .print("Book 4 stock = ",B4Stock);
	  
	  .send(jomi,askOne,delivery_options(6,1),R);
	  .print("Delivery options are ",R);
      
      .send(login,achieve,user_logout(jomi));
      
      .print(end).
      
+!show_books([]).
+!show_books([C|R]) 
   <- .send(stockManager,askOne,book(C,B),book(_,B));
      .print("  - ",B);
	  !show_books(R).

