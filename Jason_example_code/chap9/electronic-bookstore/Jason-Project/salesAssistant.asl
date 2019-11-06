// this agent interacts with the client
// each online user has one instance of this code


// some default user profile (UserName, ProfileId)
user_profile(daniel,fiction).
user_profile(jomi,mas).
user_profile(guest,news).

!check_profile.

/* plans */

// add default profile, if none is defined
+!check_profile
   :  .my_name(User) & user_profile(User,_)
   <- .send(login,askOne,client(User)).
+!check_profile
   :  .my_name(User) & not user_profile(User,_)
   <- +user_profile(User,news);
      .send(login,askOne,client(User)).

// answer for book suggestion based on profile 
+!kqml_received(S, askOne, book_suggestion, M)
	:	.my_name(User) & user_profile(User, Profile)
	<-	.send(stockManager, askOne, profile(Profile,_), profile(_,L));
		.send(S,tell,L,M).
+!kqml_received(S, askOne, book_suggestion, M)
	<-	.send(S,tell,[],M).

    
/* Book finding protocol */

// find books (not implemented, it just delegates to stockManager)
+?find_book(KeyWord,L)
	<-	.send(stockManager, askOne, find_book(KeyWord,L),find_book(KeyWord,L)); .print(L).

        
/* Book ordering protocol
      . credit card transactions is not implemented
*/

+!kqml_received(S, askOne, delivery_options(BookId,Qty), M)
    :   .my_name(User) & client(Name, Address, Uptown, City, ZipCode, State, Phone, EMail) 
	<-	.send(stockManager, askOne, book(BookId,_), book(_,BookDetails));
        BookDetails = book(BookId,Title, Authors, Publisher, Year, Genders, Price, Image, Weight)[stock(Stock)];
        // ask deliveryManager for the price
        .send(deliveryManager, askOne, delivery_options(BookId, Qty, Weight, ZipCode), DelOpt);
        .send(S, tell, delivery_confirm(client(Name, Address, Uptown, City, ZipCode, State, Phone, EMail),
                                        BookDetails,
                                        DelOpt), 
              M).

+purchase(BookId,Qty,DeliveryOption)
    :   .date(YY,MM,DD)
	<-	// tell deliveryManager
        .send(deliveryManager, tell, purchase(BookId,Qty,DeliveryOption));
        // remove purchase from BB (it was a message from the interface and do not have to be persisted)
        -purchase(BookId,Qty,DeliveryOption);
        // remember the purchase
        +purchase(BookId,Qty,DeliveryOption,date(YY,MM,DD)).

