<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Stock</title>

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
<title>Stock</title>
</head>
<a href="managerMenu.jsp"><img src="image/CabecalhoManager.jpg"></a>
<body>
<hr size=2>
<h2 align="center"><span class="style2">Stock</h2>

<%

Message     msg, msgCB;
Literal     cont, contCB;
Message     answer, answerCB;
String      content, contentCB, codeBookLis;
ListTerm    listBooksCB;
Iterator    iterCB;
Term        terms;

msgCB       = new Message("(ask :receiver stockManager)");
contCB      = Literal.parseLiteral("listAllBooks");

msgCB.put("content", contCB);
answerCB    =   mbox.ask(msgCB);
contentCB   =   answerCB.get("content").toString();
listBooksCB =   ListTermImpl.parseList(contentCB);
iterCB      =   listBooksCB.iterator(); %>

<span class="style1">
<table border="0"> 
<tr bgcolor="#999999">
    <th width="50" align="left"><span class="style1">Code</th>
    <th width="950" align="left"><span class="style1">Title</th>
    <th width="100" align="right"><span class="style1">Quantity</th>
</tr>
</table>

<%
while (iterCB.hasNext()) {
    codeBookLis =   iterCB.next().toString();
    msg         =   new Message("(ask :receiver stockManager)");
    cont        =   Literal.parseLiteral("consultStock("+codeBookLis+")"); 
    msg.put("content", cont);
    answer      =   mbox.ask(msg);
    content     =   answer.get("content").toString();
    
    terms       = Term.parse(content);
    String  codeBook    =   terms.getTerm(0).toString().replaceAll("\"","");
    String  title       =   terms.getTerm(1).toString().replaceAll("\"","");
    String  quantity    =   terms.getTerm(2).toString().replaceAll("\"","");

    if  (!title.equals("Book not found")) { %>
        <table> 
        <tr>
            <td width="50" align="left" bgcolor="#CCCCCC"><span class="style1"><%= codeBook %></td>
            <td width="950" align="left" bgcolor="#CCCCCC"><span class="style1"><%= title %></td>
            <td width="100" align="right" bgcolor="#CCCCCC"><span class="style1"><%= quantity %></td>
        </tr>    
        </table>
<%  }   
}
%>

</body>
</span>
</html>
