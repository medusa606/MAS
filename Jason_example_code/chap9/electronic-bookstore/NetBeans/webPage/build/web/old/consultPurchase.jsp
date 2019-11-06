<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<style type="text/css">
<!--
.style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt}
-->
<!--
.style2 {font-family: Arial, Helvetica, sans-serif; font-size:15pt}
-->
</style>

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>Sales</title>
</head>
<a href="managerMenu.jsp"><img src="image/Cabecalho.jpg"></a>
<body>
<hr size=2>
<h2 align="center"><span class="style2">Sales</h2>

<%

Message     msg, msgCD;
Literal     cont, contCD;
Message     answer, answerCD;
String      content, contentCD, codeDeliLis;
ListTerm    listDeliCD;
Iterator    iterCD;
Term        terms;

msgCD       = new Message("(ask :receiver deliveryManager)");
contCD      = Literal.parseLiteral("getDelivery");

msgCD.put("content", contCD);
answerCD    =   mbox.ask(msgCD);
contentCD   =   answerCD.get("content").toString();
listDeliCD  =   ListTermImpl.parseList(contentCD);
iterCD      =   listDeliCD.iterator();

while (iterCD.hasNext()) {
    codeDeliLis =   iterCD.next().toString();
    msg         =   new Message("(ask :receiver deliveryManager)");
    cont        =   Literal.parseLiteral("consultDelivery("+codeDeliLis+")");
    msg.put("content", cont);
    answer      =   mbox.ask(msg);
    content     =   answer.get("content").toString();
    
    terms       = Term.parse(content);
    
    String  codePurc    =   terms.getTerm(0).toString().replaceAll("\"","");
    String  codeBook    =   terms.getTerm(1).toString().replaceAll("\"","");
    String  qtBook      =   terms.getTerm(2).toString().replaceAll("\"","");
    String  zipCode     =   terms.getTerm(3).toString().replaceAll("\"","");
    String  totPurchase =   terms.getTerm(4).toString().replaceAll("\"","");
    String  name        =   terms.getTerm(5).toString().replaceAll("\"","");
    String  address     =   terms.getTerm(6).toString().replaceAll("\"","");
    String  uptown      =   terms.getTerm(7).toString().replaceAll("\"","");
    String  city        =   terms.getTerm(8).toString().replaceAll("\"","");
    String  state       =   terms.getTerm(9).toString().replaceAll("\"","");
    String  status      =   terms.getTerm(10).toString().replaceAll("\"","");
    String  titleBook   =   terms.getTerm(11).toString().replaceAll("\"","");  %>
    
    <span class="style1">
    <b> Code:       <%= codePurc %>     </b><br>
    <font color="#FF0000">
    <b> Status:     <%= status %>       </b><br></font>
    <b> Book:       <%= codeBook %> - <%= titleBook %> </b><br>
    <b> Total:      <%= totPurchase %>  </b><br>
    
    <b> Name:       <%= name %>         </b><br>
    <b> Address:    <%= address %>      </b><br>
    <b> Uptown:     <%= uptown %>       </b><br>
    <b> City:       <%= city %>         </b><br>
    <b> Zip code:   <%= zipCode %>      </b><br>
    <b> State:      <%= state %>        </b><br><p>
    <p><button value="alterStatus" type="button" onclick="JavaScript: window.location.href = 'alterStatus.jsp?codePurc=<%= codePurc %>';">Alter status</button></p>
<% } %>

</body>
</html>