<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Clients</title>

<style type="text/css">
<!--
.style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt;
}
-->
<!--
.style2 {font-family: Arial, Helvetica, sans-serif; font-size:15pt}
-->
</style>

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Books</title>
</head>
<a href="managerMenu.jsp"><img src="image/CabecalhoManager.jpg"></a>
<body>
<hr size=2>
<h2 align="center"><span class="style2">Clients</h2>

<%

Message     msg, msgCodeCli;
Literal     cont, contCli;
Message     answer, answerCli;
String      content, contentCli, codeCliLis;
ListTerm    listClients;
Iterator    iterClient;
Term        terms;

msgCodeCli       = new Message("(ask :receiver salesAssistant)");
contCli      = Literal.parseLiteral("listAllClient");

msgCodeCli.put("content", contCli);
answerCli    =   mbox.ask(msgCodeCli);
contentCli   =   answerCli.get("content").toString();
listClients =   ListTermImpl.parseList(contentCli);
iterClient      =   listClients.iterator();

while (iterClient.hasNext()) {
    codeCliLis =   iterClient.next().toString();
    msg         =   new Message("(ask :receiver salesAssistant)");
    cont        =   Literal.parseLiteral("getInformClient("+codeCliLis+")");
    msg.put("content", cont);
    answer      =   mbox.ask(msg);
    content     =   answer.get("content").toString();
    
    terms       = Term.parse(content);
    
    String  sequence    =   terms.getTerm(0).toString().replaceAll("\"","");
    String  userName    =   terms.getTerm(1).toString().replaceAll("\"","");
    String  password    =   terms.getTerm(2).toString().replaceAll("\"","");
    String  name        =   terms.getTerm(3).toString().replaceAll("\"","");
    String  address     =   terms.getTerm(4).toString().replaceAll("\"","");
    String  uptown      =   terms.getTerm(5).toString().replaceAll("\"",""); 
    String  city        =   terms.getTerm(6).toString().replaceAll("\"","");
    String  zipCode     =   terms.getTerm(7).toString().replaceAll("\"","");
    String  state       =   terms.getTerm(8).toString().replaceAll("\"","");
    String  phone       =   terms.getTerm(9).toString().replaceAll("\"","");
    String  eMail       =   terms.getTerm(10).toString().replaceAll("\"","");
    String  rG          =   terms.getTerm(11).toString().replaceAll("\"",""); %>
    
    <span class="style1">
    <font color="#FF0000">
    <b> Code:       <%= sequence %>     </b><br></font>
    <b> Username:   <%= userName %>     </b><br>
    <b> Name:       <%= name %>         </b><br>
    <b> Address:    <%= address %>      </b><br>
    <b> Uptown:     <%= uptown %>       </b><br>
    <b> City:       <%= city %>         </b><br>
    <b> Zip code:   <%= zipCode %>      </b><br>
    <b> State:      <%= state %>        </b><br>
    <b> Phone:      <%= phone %>        </b><br>
    <b> eMail:      <%= eMail %>        </b><br>
    <b> Register:   <%= rG %>           </b><br></p><p><p>
<%  
}
%>

</body>
</span>
</html>
