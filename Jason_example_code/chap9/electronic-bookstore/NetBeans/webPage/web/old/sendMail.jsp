<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Send mail</title>

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
<h2 align="center"><span class="style2">Send mail</h2>

<%

Message     msg, msgCB;
Literal     cont, contCB;
Message     answer, answerCB;
String      content, contentCB, codeBookLis;
ListTerm    listBooksCB;
Iterator    iterCB;
Term        terms;

msgCB       = new Message("(ask :receiver customerRelations)");
contCB      = Literal.parseLiteral("getUserSendMail");

msgCB.put("content", contCB);
answerCB    =   mbox.ask(msgCB);
contentCB   =   answerCB.get("content").toString();
listBooksCB =   ListTermImpl.parseList(contentCB);
iterCB      =   listBooksCB.iterator();

while (iterCB.hasNext()) {
    codeBookLis =   iterCB.next().toString();
    msg         =   new Message("(askOne :receiver customerRelations)");
    cont        =   Literal.parseLiteral("getInformSendMail("+codeBookLis+")");
    msg.put("content", cont);
    answer      =   mbox.ask(msg);
    content     =   answer.get("content").toString();
    
    terms       = Term.parse(content);
    
    String  name    =   terms.getTerm(0).toString().replaceAll("\"","");
    String  title   =   terms.getTerm(1).toString().replaceAll("\"","");
    String  mail    =   terms.getTerm(2).toString().replaceAll("\"","");
        
    %>
        <span class="style1">
        <b> Name:      <%= name %>        </b><br>
        <b> Title:     <%= title %>       </b><br>
        <b> E-Mail:    <a href="mailto:<%= mail %>"><%= mail %></a></b><br><p><p>
 
<%     
}
%>

</body>
</span>
</html>
