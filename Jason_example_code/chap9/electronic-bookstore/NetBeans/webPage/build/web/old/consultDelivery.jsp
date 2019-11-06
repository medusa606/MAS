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
<title>Congratulations!!!</title>
</head>
<a href="menu.jsp?codeUserURL=<%= request.getParameter("codeClient") %>"><img src="image/Cabecalho.jpg"></a>
<body>

<%
String      codeClient  = request.getParameter("codeClient");

Message     msg, msgCD;
Literal     cont, contCD;
Message     answer, answerCD;
String      content, contentCD, codeDeliLis;
ListTerm    listDeliCD;
Iterator    iterCD;
Term        terms;

msgCD       = new Message("(ask :receiver deliveryManager)");
contCD      = Literal.parseLiteral("getCodeDelivery("+codeClient+")");

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
    
    <h2 align="center"><span class="style2">Purchase code <font color="#FF0000"><%= codePurc %></font></h2>
    <h2 align="center"><span class="style2">Status <font color="#FF0000"><%= status %></font></h2>
   
    <h2 align="center"><span class="style2">Book</h2>
    <table  width="900" border="0">
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Title:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= titleBook %></span></b></label>
            </td>
        </tr>
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Quantity:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= qtBook %></span></b></label>
            </td>
        </tr>
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Price:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= totPurchase %></span></b></label>
            </td>
        </tr>
    </table>
    
    <h2 align="center"><span class="style2">Delivery</h2>
    <table  width="900" border="0">
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Name:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= name %></span></b></label>
            </td>
        </tr>
        <tr>
        <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Address:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= address %></span></b></label>
            </td>
        </tr>
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">City:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= city %></span></b></label>
            </td>
        </tr>
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Uptown:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= uptown %></span></b></label>
            </td>
        </tr>
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">State:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= state %></span></b></label>
            </td>
        </tr>
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Zipcode:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= zipCode %></span></b></label>
            </td>
        </tr>
    </table>
    <p>
    <p><button value="Buy" type="button" onclick="JavaScript: window.location.href = 'problemPurchase.jsp?codePurc=<%= codePurc %>&name=<%= name %>&titleBook=<%= titleBook %>&codeClient=<%= codeClient %>';">I have problem</button></p>
    <hr size=2>
    <%
}
%>

</body>
</html>