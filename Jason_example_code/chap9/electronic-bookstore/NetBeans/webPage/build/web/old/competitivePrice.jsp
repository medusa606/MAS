<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<a href="managerMenu.jsp"><title>Competitve price</title>
<style type="text/css">
<!--
.style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt;
}
-->
<!--
.style2 {font-family: Arial, Helvetica, sans-serif; font-size:15pt}
-->
</style>

</head>
<img src="image/CabecalhoManager.jpg"></a>
<body>
<h1 align="center"><span class="style2">Competitve price</h1></span>

<span class="style1">


<%
Message     msg, msgCB;
Literal     cont, contCB;
Message     answer, answerCB;
String      content, codeBookLis;
String contentCB = "";
ListTerm    listBooksCB;
Iterator    iterCB;
Term        terms;

msgCB       = new Message("(ask :receiver stockManager)");
contCB      = Literal.parseLiteral("getCodeAmazon");
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
    <th width="100" align="right"><span class="style1">Price</th>
</tr>
</table>

<%
while (iterCB.hasNext()) {
    codeBookLis =   iterCB.next().toString().replaceAll("\"","");;
    msg         =   new Message("(ask :receiver stockManager)");
    cont        =   Literal.parseLiteral("showBookAma("+codeBookLis+")");
    
    msg.put("content", cont);
    answer      =   mbox.ask(msg);
    content     =   answer.get("content").toString();
    terms       = Term.parse(content);
    
    String  code    =   terms.getTerm(0).toString().replaceAll("\"","");
    String  title   =   terms.getTerm(1).toString().replaceAll("\"","");
    String  author  =   terms.getTerm(2).toString().replaceAll("\"","");
    String  price   =   terms.getTerm(3).toString().replaceAll("\"","");
    %>
    <table> 
    <tr>
        <td width="50" align="left" bgcolor="#CCCCCC"><span class="style1"><%= code %></td>
        <td width="950" align="left" bgcolor="#CCCCCC"><span class="style1"><%= title %></td>
        <td width="100" align="right" bgcolor="#CCCCCC"><span class="style1"><%= price %></td>
    </tr>    
    </table>
<%   }

%>
<button align="center" value="alterPrice" type="button" onclick="JavaScript: window.location.href = 'listBooks.jsp';">Alter price</button></td>
</body>
</span>
</html>
