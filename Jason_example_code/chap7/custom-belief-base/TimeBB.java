import jason.asSemantics.*;
import jason.asSyntax.*;
import jason.bb.*;
import java.util.*;

public class TimeBB extends DefaultBeliefBase {

  private long start;

  @Override
  public void init(Agent ag, String[] args) {
     start = System.currentTimeMillis();
     super.init(ag,args);
  }

  @Override
  public boolean add(Literal bel) {
     if (! hasTimeAnnot(bel)) {
        Structure time = new Structure("add_time");
        long pass = System.currentTimeMillis() - start;
        time.addTerm(new NumberTermImpl(pass));
        bel.addAnnot(time);
     }
     return super.add(bel);
  }

  private boolean hasTimeAnnot(Literal bel) {
     Literal belInBB = contains(bel);
     if (belInBB != null)
        for (Term a : belInBB.getAnnots())
           if (a.isStructure())
              if (((Structure)a).getFunctor().equals("add_time"))
                 return true;
     return false;
  }
}
