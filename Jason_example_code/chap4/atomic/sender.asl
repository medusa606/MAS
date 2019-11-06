!send(100).                  // initial goal
+!send(0) : true <- true.    // stop sending
+!send(X) : true
   <- .send(rec,tell,vl(X)); // send value to rec
      !send(X-1).            // send next value
	  
