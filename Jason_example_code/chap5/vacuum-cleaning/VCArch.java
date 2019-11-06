import jason.asSyntax.*;
import jason.asSemantics.*;
import jason.architecture.*;
import java.util.*;

public class VCArch extends AgArch {

   @Override
   public Collection<Literal> perceive() {

      // gets the default perception
      Collection<Literal> per = super.perceive();

      // perception is null when nothing
	  // has changed in the environment
	  if (per != null) {
        Iterator<Literal> ip = per.iterator();
        while (ip.hasNext()) {
          Literal l = ip.next();
          if (l.getFunctor().equals("pos")) {
			  ip.remove();
          }
        }
	  }
	  return per;
   }

   @Override
   public void act(ActionExec action) {
       String afunctor = action.getActionTerm().getFunctor();
	   if (afunctor.equals("left") || afunctor.equals("right")) {
		   // pretend that the action was successfully performed
		   action.setResult(true);
		   getTS().getC().addFeedbackAction(action);
		   getTS().getLogger().info("not performed!");
	   } else {
		   // calls the default implementation
		   super.act(action);
	   }
   }
}
