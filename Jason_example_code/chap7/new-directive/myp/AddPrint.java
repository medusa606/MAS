package myp;

import jason.asSemantics.*;
import jason.*;
import jason.asSyntax.*;
import jason.asSyntax.directives.*;
import jason.asSyntax.PlanBody.BodyType; 

public class AddPrint implements Directive { 

    public Agent process(Pred directive, 
	                     Agent outterContent, 
                         Agent innerContent) { 
        try {
            Agent newAg = new Agent();
			newAg.initAg();
            Term arg = directive.getTerm(0); // get the parameter 
            for (Plan p:innerContent.getPL()) { 
                // create the new command .print(X) -- a body literal 
                Literal print = ASSyntax.createLiteral(".print"); 
                print.addTerm(arg.clone()); 
                PlanBody pb = new PlanBodyImpl(BodyType.internalAction, print); 
                p.getBody().add(pb);  // appends the new formula to the plan
                newAg.getPL().add(p); // includes the plan in the PL
            }
            return newAg; 
		} catch (JasonException je) {
			je.printStackTrace();
		}
		return null;		
    } 
} 

