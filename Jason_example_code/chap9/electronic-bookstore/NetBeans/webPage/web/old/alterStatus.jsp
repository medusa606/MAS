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
<title>Alter status</title>
</head>
<a href="managerMenu.jsp"><img src="image/CabecalhoManager.jpg"></a>
<body>

<%
String  codePurchase= request.getParameter("codePurc");
Message msg;
Literal cont;
Message answer;
String  content;
        
if  (request.getParameter("status") != null) {
    String  status  =   request.getParameter("status");   
    if  (!status.equals("")){
        msg         =   new Message("(ask :receiver deliveryManager)");
        cont        =   Literal.parseLiteral("alterStatus("+codePurchase+",\""+status+"\")");
        msg.put("content", cont);
        answer      =   mbox.ask(msg);
        content     =   answer.get("content").toString();
     }
}

msg         =   new Message("(ask :receiver deliveryManager)");
cont        =   Literal.parseLiteral("consultDelivery("+codePurchase+")");
msg.put("content", cont);
answer      =   mbox.ask(msg);
content     =   answer.get("content").toString();

Term    terms       = Term.parse(content);

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
   
<form id="alterStatus" name="alterStatus" method="post" action="">

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

<table  width="900" border="0">
    <tr>
        <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Alter status:</span></label>
        </td>
        <td width="110" align="left" valign="middle">
            <span class="style1">
            <select name="status">
            <option selected>
            <option value="Processed">Processed
            <option value="Waiting sending">Waiting sending
            <option value="Correspondent">Correspondent
            <option value="Give">Give
            <option value="Problem">Problem
        </td>
        <td>
            <text></text><input name="sbmtStatus" type="submit" value="Confirm"/>
            </select>
            </span>
        </td>
    </tr>
</table>
</form>

</body>
</html>