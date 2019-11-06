package math;

import jason.asSemantics.*;
import jason.asSyntax.*;
import java.util.*;

public class odd extends DefaultInternalAction {

  @Override
  public Object execute(TransitionSystem ts, 
                        final Unifier un, 
                        final Term[] arg) throws Exception {
                 
     if (! arg[0].isVar()) {
        // the argument is not a variable, single answer
        if (arg[0].isNumeric()) {
           NumberTerm n = (NumberTerm)arg[0];
           return n.solve() % 2 == 1;
        } else {
           return false;
        }

     } else { 

        // returns an iterator of unifiers,
        // each unifier has the arg[0] (a variable)
        // assigned to an odd number.

        return new Iterator<Unifier>() {
           int last = 1; 

           // we always have a next odd number
           public boolean hasNext() { return true; }

           public Unifier next() {
               Unifier c = (Unifier)un.clone();
               c.unifies(new NumberTermImpl(last), arg[0]);
               last += 2;
               return c;
           }

           public void remove() {}
        };
} }  }
