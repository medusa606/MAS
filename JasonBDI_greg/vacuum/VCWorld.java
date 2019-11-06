import jason.asSyntax.*;
import jason.environment.*;
import java.util.logging.*;
import java.util.*;
import javax.swing.*;
import java.awt.*;
import javax.swing.border.*;

//package net.codejava.io;
import java.io.FileWriter; //for writing csv file
import java.io.PrintWriter; //for writing csv file
import java.io.IOException; //for file writing errors 
import java.io.BufferedWriter;




 
public class VCWorld extends Environment {

    /** world model */
	// sets out the map grid
    private boolean[][] dirty = { 
		{ true, true, true, true, true, true },
		{ true, true, true, true, true, true },
		{ true, true, true, true, true, true },
		{ true, true, true, true, true, true },
		{ true, true, true, true, true, true },
		{ true, true, true, true, true, true },	
	};

	//set (or read) initial location of the agent
	private Random   r = new Random();
	private int vcx = r.nextInt(6);//set a random location
    private int vcy = r.nextInt(6);
	
	int ran_dir = r.nextInt(4);
	//logger.info("The random direction is ");//+ran_dir+"."
	//logger.info("suck in a clean location!");
		
	private int avx = 2; // the AV location
    private int avy = 5;
	


    private Object modelLock = new Object(); 

    /** general delegations */
    private HouseGUI gui = new HouseGUI();
    private Logger   logger = Logger.getLogger("env."+VCWorld.class.getName());

    /** constant terms used for perception */
    private static final Literal lPos1  = ASSyntax.createLiteral("pos", ASSyntax.createNumber(1));
    private static final Literal lPos2  = ASSyntax.createLiteral("pos", ASSyntax.createNumber(2));
    private static final Literal lPos3  = ASSyntax.createLiteral("pos", ASSyntax.createNumber(3));
    private static final Literal lPos4  = ASSyntax.createLiteral("pos", ASSyntax.createNumber(4));
    private static final Literal lDirty = ASSyntax.createLiteral("dirty");
    private static final Literal lClean = ASSyntax.createLiteral("clean");

    public VCWorld() {
        createPercept();
        
        // create a thread to add dirty
        new Thread() {
            public void run() {
                try {
                    while (isRunning()) {
                        // add random dirty
                        if (r.nextInt(100) < 20) { 
                            dirty[r.nextInt(2)][r.nextInt(2)] = true;
                            gui.paint();
                            createPercept();
                        }
                        Thread.sleep(1000);
                    }
                } catch (Exception e) {} 
            }
        }.start();  
    }
        
    /** create the agents perceptions based on the world model */
    private void createPercept() {
        // remove previous perception
        clearPercepts();       
		
        //create percepts of "on pavement", "AV nearby" etc.
        if (vcx == 0 && vcy == 0) {
            addPercept(lPos1);
        } else if (vcx == 1 && vcy == 0) {
            addPercept(lPos2);
        } else if (vcx == 0 && vcy == 1) {
            addPercept(lPos3);
        } else if (vcx == 1 && vcy == 1) {
            addPercept(lPos4);
        }

        if (dirty[vcx][vcy]) {
            addPercept(lDirty);
        } else {
            addPercept(lClean);
        }
    }

    @Override
    public boolean executeAction(String ag, Structure action) {
        logger.info("doing "+action);
        
        try { Thread.sleep(500);}  catch (Exception e) {} // slow down the execution
        
        synchronized (modelLock) {
            // Change the world model based on action
            if (action.getFunctor().equals("suck")) {
                if (dirty[vcx][vcy]) {
                    dirty[vcx][vcy] = false;
                } else {
                    logger.info("suck in a clean location!");
                    Toolkit.getDefaultToolkit().beep();
                }
            } else if (action.getFunctor().equals("left")) {
                if (vcx > 0) {
                    vcx--;
                }
            } else if (action.getFunctor().equals("right")) {
                if (vcx < dirty.length) {
                    vcx++;
                }
            } else if (action.getFunctor().equals("up")) {
                if (vcy > 0) {
                    vcy--;
                }
			}
			else if (action.getFunctor().equals("av_up")) {
                if (avy > 0) {
                    avy--; // move the AV up only
                }
				if(avy==5){avy=0;} //reset position

				
            } else if (action.getFunctor().equals("down")) {
                if (vcy < dirty.length) {
                    vcy++;
					//logger.info("moving to "+vcy+".");

                }
			} else if (action.getFunctor().equals("mv_rand")) {
			
				
				//get a random number 1-4 to choose direction
				int ran_dir = r.nextInt(4);
				//logger.info("The random direction is "+ran_dir+".");
					
				/*add this to the current index
				switch (ran_dir){
					case 0: vcx--;break;
					case 1: vcx++;break;
					case 2: vcy--;break;
					case 3: vcy++;break;}*/
					
				//add this to the current index
				switch (ran_dir){
					case 0: 
						if (vcx<1){
							vcx++;
							logger.info("The random direction is right.");
							break;
						}else{
							vcx--;
							logger.info("The random direction is left.");
							break;}
					case 1: 
						if (vcx>4){
							vcx--;
							logger.info("The random direction is left.");
							break;
						} else {
							vcx++;	
							logger.info("The random direction is right.");
						break;}
					case 2: 
						if (vcy<1){
							vcy++;
							logger.info("The random direction is down.");
							break;
						} else {
							vcy--; 
							logger.info("The random direction is up.");
						break;}
					case 3: 
						if (vcy>4){
							vcy--;
							logger.info("The random direction is up.");
							break;
						} else {
							vcy++;
							logger.info("The random direction is down.");
							break;}
				} 
				/*else if (action.getFunctor().equals("rand_behav")) {
			
				
				//get a random number 1-2 to choose behaviour
				
				//execute either behaviour
				
				}*/
				
	
			
            } else {
                logger.info("The action "+action+" is not implemented!");
                return false;
            }
        }
        
        createPercept(); // update agents perception for the new world state      
        gui.paint();
		
		String content = "This is the content to write into file\n";
		// If the file exists, truncate (remove all content) and write to it
		try (FileWriter writer = new FileWriter("app.log", true);
			 BufferedWriter bw = new BufferedWriter(writer)) {	
			bw.write(content);	
		} catch (IOException e) {
			System.err.format("IOException: %s%n", e);
		}
		//log test 2
		content = "this is NEW content\n";
		bw.write(content);
		
		//check if AV is at end of map  TODO
		if (avy==0)){
		logger.info("AV at end of map");
		stop();}
		
		//check assertion
		if (vcx==avx && vcy==avy){
		logger.info("Ped and AV at same location");
		stop();} //need to exit cleanly - this doesn't work that well  TODO
        return true;
    }
    
    @Override
    public void stop() {
        super.stop();
        gui.setVisible(false);
    }
    
    
    /* a simple GUI */ 
    class HouseGUI extends JFrame {
        JLabel[][] labels;
        
        HouseGUI() {
            super("Domestic Robot");
            labels = new JLabel[dirty.length][dirty.length];
            getContentPane().setLayout(new GridLayout(labels.length, labels.length));
            for (int j = 0; j < labels.length; j++) {
                for (int i = 0; i < labels.length; i++) {
                    labels[i][j] = new JLabel();
                    labels[i][j].setPreferredSize(new Dimension(180,180));
                    labels[i][j].setHorizontalAlignment(JLabel.CENTER);
                    labels[i][j].setBorder(new EtchedBorder());
                    getContentPane().add(labels[i][j]);
                }
            }
            pack();
            setVisible(true);
            paint();
        }
        
        void paint() {
            synchronized (modelLock) { // do not allow changes in the robot location while painting
                for (int i = 0; i < labels.length; i++) {
                    for (int j = 0; j < labels.length; j++) {
                        String l = "<html><center>";
                        if (vcx == i && vcy == j) {
                            l += "<font color=\"red\" size=7><b>Ped</b><br></font>";
                        }
						if (avx == i && avy == j) {
                            l += "<font color=\"green\" size=7><b>AV</b><br></font>";
                        }
						//add Road and Pavement tags
                        if (i<2) {l += "<font color=\"blue\" size=5>pavement</font>";}
						if (i>3) {l += "<font color=\"blue\" size=5>pavement</font>";}
						
                        l += "</center></html>";
                        labels[i][j].setText(l);
                    }
                }
            }
        }
    }    
}

