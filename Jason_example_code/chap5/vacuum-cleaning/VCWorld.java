import jason.asSyntax.*;
import jason.environment.*;
import java.util.logging.*;
import java.util.*;

/** Simple Vacuum cleaning environment */
public class VCWorld extends Environment {

   // dirty[0] is the left loc, dirty[1] the right
   boolean[] dirty = { true, true };
   
   // the vacuum cleaner is in the left
   char vcPos = 0;
   
   Random r = new Random();
   Logger logger = Logger.getLogger("env.VC");

   @Override 
   public void init(String[] args) {
      updatePercepts();
   }

   /** update the agent's percepts based on the current
       state of the world model */
   private void updatePercepts() {
      // dynamically add dirty
      if (r.nextInt(100) < 20) {
         dirty[r.nextInt(2)] = true;
      }
      clearPercepts();    // remove previous percepts
      if (dirty[vcPos]) { // 'dirty' must be added before position as
                          // the agent model assumes this order is used
         addPercept(Literal.parseLiteral("dirty"));
      } else {
         addPercept(Literal.parseLiteral("clean"));
      }
      if (vcPos == 0) {
         addPercept(Literal.parseLiteral("pos(l)"));
      } else if (vcPos == 1) {
         addPercept(Literal.parseLiteral("pos(r)"));
      }
   }

   /** changes the world model according to agent actions */
   @Override
   public boolean executeAction(String ag, Structure action) {
      // action: suck
      if (action.getFunctor().equals("suck")) {
         if (dirty[vcPos]) 
            dirty[vcPos] = false;  // note perception is accurate
      // action: left
      } else if (action.getFunctor().equals("left")) {
         if (vcPos > 0) 
            vcPos--;
      // action: right
      } else if (action.getFunctor().equals("right")) {
         if (vcPos+1 < dirty.length) 
            vcPos++;
      // unknown action
      } else {
         logger.info("Action "+action+" is not implemented!");
         return false;
      }

      updatePercepts(); // update the agent's percepts for the new
                        // state of the world (after this action)
      return true;      // in this model, all actions succeed
   }
}