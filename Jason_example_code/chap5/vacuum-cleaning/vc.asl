/*

Very simple vaccum cleaner agent in a world that has only two locations.

Perceptions:
. dirty: the current location has dirty
. clean: the current location is clean
. pos(X): the agent position is X, where X is either l or r.

Actions:
. suck: clean the current location
. left: go to the left positions
. right: go to the right position

*/

// in case I am in a dirty location
+dirty: true <- suck.

// in case I am in a clean location
+clean: pos(l) <- right.
+clean: pos(r) <- left.


/*
// another soluton (independent of the order of perceptions)
+dirty: true <- suck.
+clean: pos(l) <- -clean; right.
+clean: pos(r) <- -clean; left.
*/

/* // yet another soluton (independent of the order of perceptions)
+dirty: true <- suck; !move.
+pos(_) : not dirty <- !move.

+!move : pos(l) <- right.
+!move : pos(r) <- left.
*/
