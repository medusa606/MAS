// creates an agent for each logged user

/* beliefs */

// initial client data
// client(UserName, Password, Name, Address, Uptown, City, ZipCode, State, Phone, EMail)
client(  	daniel,	
			"daniel",	
			"Daniel Dalcastagne",	
			"Rua 21 de Junho, 535",	
			"Centro", 
			"Ilhota",
			"88320000",
			"SC", 
			"3343-1138",
			"dalcastagne@gmail.com").
				
client( 	adriana,	
			"adriana",	
			"Adriana Cordeiro",	
			"Rua 21 de Junho, 2038",
			"Centro", 
			"Ilhota",
			"88320000",
			"SC", 
			"3343-1204",
			"adriana@gmail.com").
				
client( 	jomi,	
			"fred",	
			"Jomi F. Hubner",	
			"Rua Florida, 520",	
			"Velha", 
			"Blumenau", 
			"89041250",
			"SC", 
			"3330-1516",
			"jomifred@gmail.com").
                
/* plans */

// client managing

+!kqml_received(S, askOne, add_client(UserName, Password, Name, Address, Uptown, City, ZipCode, State, Phone, EMail), M)
	:	not client(UserName, _, _, _, _, _, _, _, _, _) 
	<-	+client(UserName, Password, Name, Address, Uptown, City, ZipCode, State, Phone, EMail);
		.send(S, tell, ok, M);
		.print("Add client: ", Name, " code: ", Id).
		
+!kqml_received(S, askOne, add_client(UserName, _, _, _, _, _, _, _, _, _), M)
	:	client(UserName, _, _, _, _, _, _, _, _, _)
	<-	.send(S, tell, error("Invalid username"), M);
		.print("Invalid username").

+!kqml_received(S, askOne, client(UserName),M)
	:	client(UserName, Password, Name, Address, Uptown, City, ZipCode, State, Phone, EMail)	
	<-	.send(S, tell, client(Name, Addres, Uptown, City, ZipCode, State, Phone, EMail), M).

+!kqml_received(S, askOne, user_logon(UserName, Password), M)
	:	client(UserName, Password, Name, _, _, _, _, _, _, _)
	<-	// creates an agent for this user
        .create_agent(UserName,"saleAssistant.asl");
        .send(UserName, tell,user_name(UserName)); // tell this new agent its user
        .send(S, tell, client(Name), M);
		.print(Name, " login").
				
+!kqml_received(S, askOne, user_logon(UserName, Password), M)
	<-	.send(S, tell, error("Username or password invalid!"), M).

+!kqml_received(S, askAll, client_ids, M)
	<-	.findall(Id,client(Id, _, _, _, _, _, _, _, _, _, _),ListClient);
		.send(S, tell, ListClient, M);
		.print("All clients ", ListClient).
		
