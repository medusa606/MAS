import jason.asSemantics.*;
import jason.asSyntax.*;
import java.util.*;

public class DirtyFocusAgent extends Agent {

   static Trigger focus = Trigger.parseTrigger(
                          "+dirty[source(percept)]");
   
   @Override
   public Event selectEvent(Queue<Event> events) {
      Iterator<Event> i = events.iterator();
      while (i.hasNext()) {
         Event e = i.next(); 
         if (e.getTrigger().equals(focus)) {
           i.remove();
           return e;
         }
      }
      return super.selectEvent(events);
   }
}
