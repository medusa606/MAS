Implementation of the Electronic Bookstore using Jason
------------------------------------------------------

This MAS was specified using Prometheus methodology in the book
'Developing Intelligent Agent Systems' by Lin Padgham and Michael
Winikoff. In the doc directory there is a copy of the system
specification.

Only part of the system is implemented, since it is not entirely
finished in the Padgham et al. book. The first version of this system was
implemented by Daniel Dalcastagne in his undergraduate course and
after updated by Jomi F. Hubner.

The implemented functionalities are:
. Online interaction
. Welcoming
. Book finding
. Purchasing
. Stock management

The agents of the system are (the first two agents are not in the
book, but useful in the implementation):

. web: it is indeed the web interface of the system, it runs in a JEE
  container and uses a SACI's MailBox to send and receive KQML
  messages to/from other agents.

. login: when an user logs into the site, this agent creates a
  salesAssistant instance for it.
  
. salesAssistant: each logged user has its own salesAssistant
  agent.

. deliveryManager (as in the book, see doc)

. stockManager (as in the book, see doc)



Requirements to run the system:
. Jason >= 1.2
. A web server to deploy the web application

Steps to run this application:

1. Open the Jason project (in folder Jason-Project, file
   electronic-bookstore.mas2j) and run it.
   The main window of SACI should open.

2. Deploy the web application (the current version was developed
   with NetBeans 5.5).
   Using Tomcat, just copy the file
      NetBeans/webPage/dist/webPage.war
   to the directory webapps of your Tomcat installation.

3. Open the web application in some browser and test it.
   http://localhost:8080/webPage

   If you want you can use the user jomi (password fred) or
   register a new user.

