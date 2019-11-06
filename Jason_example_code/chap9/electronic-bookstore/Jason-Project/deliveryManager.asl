/* beliefs */

// zip_code(ZipCode, City, State)
zip_code("88320000", "Ilhota", "SC").
zip_code("89010000", "Blumenau", "SC").
zip_code("89041250", "Blumenau", "SC").
zip_code("89252000", "Jaragua do Sul", "SC").
zip_code("89120000", "Timbo", "SC").

// rate(ZipCode destiny, Rate, Distance, Time)
zip_code_rate("88320000", 0.0090, 900, 03).
zip_code_rate("89010000", 0.0090, 850, 02).
zip_code_rate("89041250", 0.0090, 850, 02).
zip_code_rate("89252000", 0.0090, 700, 05).
zip_code_rate("89120000", 0.0080, 910, 03).

// Days to delivery (zip, days)
delivery_days("88320000", 5).
delivery_days("89010000", 6).
delivery_days("89041250", 2).
delivery_days("89252000", 7).
delivery_days("89120000", 5).

// status_code(Code, Status)
status_code(1,"Processed").
status_code(2,"Waiting sending").
status_code(3,"Correspondent").
status_code(4,"Late delivery").
status_code(5,"Give").
status_code(6,"Problem").

/* rules */

calculate_delivery(ZipCode, Weight, Qty, Price)
	:-	zip_code_rate(ZipCode, Rate, Distance, Days) &
		Weight > 0 &
        Price = (Distance*Rate*Weight*Qty).


/* plans */

// answer delivery_option with only one option!
+!kqml_received(S, askOne, delivery_options(BookId, Qty, Weight, ZipCode), M)
    :   calculate_delivery(ZipCode, Weight, Qty, Price) &
        delivery_days(ZipCode,Days)
    <-  Opts = delivery_options([option(1,Price,Days)]);
        // remember options
        +offered_option(S,zip(ZipCode),BookId,Qty,Opts);
        .send(S,tell,Opts,M).
+!kqml_received(S, askOne, delivery_options(BookId, Qty, Weight, ZipCode), M)
    <-  .send(S,tell,delivery_options([option(1,40,10)]),M).

    
+purchase(BookId,Qty,DeliveryOption)[source(User)]
    <-  // simply tells stockManager (assume that thera are books in the stock!)
        .send(stockManager, tell, delivered(BookId,Qty));
        // remove purchase from BB (it was a message from the interface and do not have to be persisted)
        -purchase(BookId,Qty,DeliveryOption);
        // remember the purchase
        .date(YY,MM,DD);
        +sale(User,BookId,Qty,DeliveryOption,date(YY,MM,DD)).
        

