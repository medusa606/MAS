<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />


Not Implemented!



<%

if (true) return;

String  codeBook    = request.getParameter("codeBook");
String  codeClient  = request.getParameter("codeClient");
String  titleBook   = request.getParameter("titleBook");
String  qtBook      = request.getParameter("qtBook");
String  zipCode     = request.getParameter("zipCode");
String  totPurchase = request.getParameter("totPurchase");
String  name        = request.getParameter("name");
String  address     = request.getParameter("address");
String  uptown      = request.getParameter("uptown");
String  city        = request.getParameter("city");
String  state       = request.getParameter("state");

Message msg         = new Message("(ask :receiver deliveryManager)");
Literal content     = Literal.parseLiteral("sale("+codeBook+","+codeClient+","+qtBook+","+zipCode+","+totPurchase+",\""+name+"\",\""+address+"\",\""+uptown+"\",\""+city+"\",\""+state+"\")");
msg.put("content", content);
Message replace     = mbox.ask(msg);
String msgRet       = "Approximate time for delivery "+replace.get("content").toString()+" days.";

%>

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

<form id="confirmBuy" name="confirmBuy" method="post" action="">
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
        <td width="450" align="left" valign="middle"><label for="textfield"><b><font color="#FF0000"><span class="style1"><%= totPurchase %></span></font></b></label>
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

<h2 align="center"><span class="style2">Delivery time</h2>
<center><b><span class="style1"><%=msgRet%></span></b></center>

</form>
</body>
</html>