<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>

<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<%

String  bookId    = request.getParameter("bookId");
String  username  = session.getAttribute("username").toString();
int     qtBook    = 1;


// get delivery options
Message m = new Message("(askOne)");
m.put("receiver",username);
m.put("content", "delivery_options("+bookId+","+qtBook+")");
Message r = mbox.ask(m);

//out.println(r);

if (! r.toString().startsWith("(tell")) {
    out.println("Error in this response!");
}
Structure content = Structure.parse(r.get("content").toString());


Structure client = (Structure)content.getTerm(0);
Structure book = (Structure)content.getTerm(1);

// delivery options = delivery_options([option(1,3.06,2)]))
Structure delOpt = (Structure)content.getTerm(2);
// get first option
Structure option1 = (Structure)((ListTerm)delOpt.getTerm(0)).get(0);


String  titleBook   = ((StringTerm)book.getTerm(1)).getString();
double  untPrice    = ((NumberTerm)book.getTerm(6)).solve();
double  totPrice    = qtBook * untPrice;
double  totFreight  = ((NumberTerm)option1.getTerm(1)).solve();
double  totPurchase = totPrice + totFreight;

int     shipIn      = (int)((NumberTerm)option1.getTerm(2)).solve();

String  name        = ((StringTerm)client.getTerm(0)).getString();
String  address     = ((StringTerm)client.getTerm(1)).getString();
String  uptown      = ((StringTerm)client.getTerm(2)).getString();
String  city        = ((StringTerm)client.getTerm(3)).getString();
String  zipCode     = ((StringTerm)client.getTerm(4)).getString();
String  state       = ((StringTerm)client.getTerm(5)).getString();

String  msgRet;

/*

if  ((request.getParameter("quantity") != null) &&
    (request.getParameter("zipCode") != null)){
    zipCode = request.getParameter("zipCode");
    qtBook  = request.getParameter("quantity");
}

if  ((zipCode.length() > 0) && (qtBook.length() > 0)) {
    msg         = new Message("(ask :receiver deliveryManager)");
    content     = Literal.parseLiteral("informPurchase("+codeBook+","+qtBook+","+zipCode+","+codeClient+")");
    msg.put("content", content);
    replace     = mbox.ask(msg);
    msgRet      = replace.get("content").toString();

    terms       = Term.parse(msgRet);

    titleBook   = terms.getTerm(0).toString().replaceAll("\"","");
    untPrice    = terms.getTerm(1).toString();
    totPrice    = terms.getTerm(2).toString();
    totFreight  = terms.getTerm(3).toString();
    totPurchase = terms.getTerm(4).toString(); 
}
*/

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
<title>Buy book</title>
</head>
<img src="image/Cabecalho.jpg"></a>
<body>

    
<form id="buyBook" name="buyBookForm" method="post" action="">

<h2 align="center"><span class="style2">Price</h2> 
<table border="1"> 
    <tr bgcolor="#999999">
        <th width="800" align="left"><span class="style1">Description</th>
        <th width="100" align="right"><span class="style1">Quantity</th>
        <th width="100" align="right"><span class="style1">Unt price</th>
        <th width="100" align="right"><span class="style1">Price</th>
    </tr>
    <tr>
        <td width="800" align="left" bgcolor="#CCCCCC"><span class="style1"><%= titleBook %></td>
        <td width="100" align="right" bgcolor="#CCCCCC"><span class="style1"><input name="quantity" align="right" value= <%= qtBook %> type="text" id="quantity" size="10" maxlength="10" /></td>
        <td width="100" align="right" bgcolor="#CCCCCC"><span class="style1"><%= untPrice %></td>
        <td width="100" align="right" bgcolor="#FF6666"><span class="style1"><b> <%= totPrice %> </b></td>
    </tr>    
</table>
<p>
<table border="1">
    <td width="980" align="left" scope="col" bgcolor="#CCCCCC"><label for="textfield"><span class="style1">Zip code</span></label>
    <input name="zipCode" type="text" id="zipCode" size="10" maxlength="10" value="<%= zipCode %>"/></td>
    <td width="100" align="right" bgcolor="#FF6666"><span class="style1"><b><%= totFreight %></b></td>
</table>
<p>
<table border="1"> 
    <tr bgcolor="#FF6666">
        <td width="980" align="left"><span class="style1"><b>Total ($)</b></td>
        <td width="100" align="right"><span class="style1"><b><%= totPurchase %></b></td>
    </tr>
</table>
<p>
<table border="0">
    <tr>
        <td width="980" align="center"><button value="Calculate" type="submit" align="center">Calculate</button></td>
    </tr>
</table>
</form> 


<form id="confirmBuyBook" name="confirmBuyBookForm" method="post" action="buyBook.jsp">
<h2 align="center"><span class="style2">Delivery place</h2> 
<table width="49" border="0" align="center">
    <tr>
        <td width="69" align="right" valign="middle"><label for="txtName"><span class="style1">Name:</span></label></td>
        <td width="354">
        <input name="txtName" type="text" id="txtName" size="50" maxlength="50" value="<%= name %>" />    </td>
    </tr>
    <tr>
        <td align="right" valign="middle"><label for="txtAddress"><span class="style1">Address:</span></label></td>
        <td><input name="txtAddress" type="text" id="txtAddress" size="50" maxlength="50" value="<%= address %>" /></td>
    </tr>
    <tr>
        <td align="right" valign="middle"><label for="txtUptown"><span class="style1">Uptown:</span></label></td>
        <td><input name="txtUptown" type="text" size="50" maxlength="50" value="<%= uptown %>" /></td>
    </tr>
    <tr>
        <td align="right" valign="middle"><label for="txtCity" class="style1">City:</label></td>
        <td><input name="txtCity" type="text" size="50" maxlength="50" value="<%= city %>" /></td>
    </tr>
    <tr>
        <td align="right" valign="middle"><label for="txtState" class="style1">State:</label></td>
        <td><input name="txtState" type="text" size="50" maxlength="50" value="<%= state %>" /></td>
    </tr>
</table>
</form>

<table width="980" border="0" align="center">
    <td align="center">
    <button align="center" value="confirmBook" type="button" onclick="JavaScript: window.location.href = 'confirmBuy.jsp?codeBook=<%= bookId %>'"> Confirm </button>
    </td>
</table>

</span>
</body>
</html>
