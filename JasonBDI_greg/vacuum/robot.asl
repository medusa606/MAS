// Pedestrian Agent
// G.Chance 4-7-19


//! Achievement Goal
//? Test Goal
//+ or - for addition or subtraction of belief

/*  
1.a Random Action
	At each time step execute random primitive
1.b Random Behaviour
	At each time step execute random behaviour
	
Behaviours are:
	Initialisation: agent moves along pavement in + or -ve direction
	Behaviours: walk, stop, cross_road, turn_around
	
Movement Primities are:
	Move: up, down, left, right, stop
	
*/

//Set which test to run
//TestID 0=1a, 1=1b, etc..
//testID=0; //get correct syntax TODO

//-----------------------------------------
//1.a Random Action
!start.
	+!start <- mv_rand;
	.print("taking random action.");
	!start.
	
//-----------------------------------------
//1.b Random Behaviour
//!randomBehav. //check for testID here...TODO
//	+!randomBehav : b(2) <- rand_behav; //need to write behaviour actions TODO
//	.print("taking random behaviour");
//	!randomBehav. //restart this action
	
	

/*+pos(1) : dirty <- suck; right.
+pos(2) : dirty <- suck; down.
+pos(3) : dirty <- suck; up.
+pos(4) : dirty <- suck; left.

// plans for clean location
+pos(1) : clean <- right.
+pos(2) : clean <- down.
+pos(3) : clean <- up.
+pos(4) : clean <- left.*/

/* // More plans
//+pos(1) : clean <- someaction; another_action.    // whenever I perceive I'm in pos(1) and
                                   					// I believe that my position is clean,
													// do some action.
+pos(_) : dirty <- suck; !move.
+pos(_) : true  <- !move.

// plans to move
+!move : pos(1) <- right.
+!move : pos(2) <- down.
+!move : pos(3) <- up.
+!move : pos(4) <- left.*/

/* Plans */
/*
!clean. // initial goal to clean
!pause. // initial goal to break

+!clean : clean <- !move; !clean.
+!clean : dirty <- suck;  !clean.
-!clean         <- !clean.

+!move : pos(1) <- right.
+!move : pos(2) <- down.
+!move : pos(3) <- up.
+!move : pos(4) <- left.

+!pause
  <- .wait(2000);     // suspend this intention (the pause) for 2 seconds
     .suspend(clean); // suspend the clean intention
     .print("I'm having a break, alright.");
     .wait(1000);     // suspend this intention again for 1 second
     .print(cleaning);
     .resume(clean);  // resume the clean intention
     !pause.
*/
