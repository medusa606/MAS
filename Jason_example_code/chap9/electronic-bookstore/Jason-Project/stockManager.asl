/* beliefs */

last_book_code(20).

// profile books (ProfileId, list of books' Id)
profile(fiction,[2]).
profile(mas,[1,4,5,6]).
profile(news,[6,1]).

/* rules */

//all_book_codes(L) 
//    :- .findall(Code,  book(Code, _, _, _, _, _, _), L).

// get book details based on a book code    
book_details(Code, book(Code, Title, Authors, Publisher, Year, Topics, Price, Image, Weight)) 
    :- book(Code, Title, PublisherId, Year, Price, Image, Weight) & 
       publisher(PublisherId, Publisher) & 
       .findall(A,book_author(Code,A),AuthorsC)  &
       author_code_name(AuthorsC,Authors) & 
       .findall(T,book_topic(Code,T), Topics).
author_code_name([],[]).
author_code_name([C|RC],[N|RN])       
    :- author(C,N) & author_code_name(RC,RN).
    
// find book with some author
find_by_author(SearchAuthor,Code)
    :-  book(Code, _, _, _, _, _, _) & // for all books in DB
        book_author(Code,AuthorId) &   // for all its authors
        author(AuthorId,Name) &        // get author's name
        .substring(SearchAuthor,Name).

// find book with some title    
find_by_title(SearchTitle,Code)
    :-  book(Code, Title, _, _, _, _, _) &
        .substring(SearchTitle,Title).
    

/* plans */

// send a mail to sales assistent to update profiles
+!kqml_received(S, tell, add_book(Title, Authors, Publisher, Year, Price, Genders, Image), M)
	:	last_book_code(Code)
	<-	-+last_book_code(Code+1);
        +book(Code, Title, Authors, Publisher, Year, Genders, Price, Image, Weight);
		+book_stock(Code, 0);
		!update_profiles(Code,Genders);
		.print("Book register: ", Title, " code: ", Sequence).

+?book(Code,Details)
	:	book_details(Code,B) & book_stock(Code, Stock)
	<-	.add_annot(B,stock(Stock),Details).	
    

/*        
+!kqml_received(S, askOne, find_book(KeyWord), M)
	<-	.findall(CA,find_by_author(KeyWord,CA),LA);
        .findall(CT,find_by_title(KeyWord,CT),LT);
        .concat(LA,LT,L); // TODO: remove duplicates
        .send(S, tell, L, M).
*/

+?find_book(Key, L)
	<-	.findall(CA,find_by_author(Key,CA),LA);
        .findall(CT,find_by_title(Key,CT),LT);
        .concat(LA,LT,L).

// update the book stock, when some was delivered        
@ld[atomic]
+delivered(BookId,Qty)
    :   book_stock(BookId,Stock) &
        Stock >= Qty
    <-  -book_stock(BookId,Stock);
        +book_stock(BookId,Stock-Qty);
        -delivered(BookId,Qty).
    
// simple profile based on gender, should be improved!
+!update_profiles(Code,[]).
+!update_profiles(Code,[Gender|RG])
    <-  !update_profile(Code,Gender);
        !update_profiles(Code,RG).
+!update_profile(Code,Gender)
    :   profile(Gender,L)
    <-  -+profile(Gender,[Code|L]).
+!update_profile(Code,Gender)
    <-  -+profile(Gender,[Code]).
    


