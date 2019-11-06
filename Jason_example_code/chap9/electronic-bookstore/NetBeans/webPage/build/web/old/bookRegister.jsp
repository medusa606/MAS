<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>

<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<%
String msg      = "";
String title    = "";
String author   = "";
String publisher= "";
String price    = "";
String image    = "";
String gender   = "";
if (request.getParameter("txtTitle") != null) {
    title       = request.getParameter("txtTitle");
    author      = request.getParameter("txtAuthor");
    publisher   = request.getParameter("txtPublisher");
    price       = request.getParameter("txtPrice");
    image       = request.getParameter("txtImage");
    gender      = request.getParameter("txtGender");
    
    Message m = new Message("(ask :receiver stockManager)");
    Literal c = Literal.parseLiteral("addBook(\""+title+"\""+",\""+author+"\",\""+publisher+"\","+price+",\""+gender+"\",\""+image+"\")");
    m.put("content", c);
    Message r = mbox.ask(m);
    msg = r.get("content").toString().replaceAll("\"","");
    
}

%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Book register</title>
<style type="text/css">
<!--
.style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt}
-->
<!--
.style2 {font-family: Arial, Helvetica, sans-serif; font-size:15pt}
-->
</style>
</head>
<a href="managerMenu.jsp"><img src="image/CabecalhoManager.jpg"></a>
<body>
<h1 align="center"><span class="style2">Book register</h1> 
<form id="bookRegisterForm" name="bookRegisterForm" method="post" action="bookRegister.jsp">
<table width="49" border="0" align="center">
  <tr>
    <td width="69" align="right" valign="middle"><label for="txtTitle"><span class="style1">Title:</span></label></td>
    <td width="354">
      <input name="txtTitle" type="text" id="txtTitle" size="50" maxlength="50" value="<%=title%>" />    </td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtAuthor"><span class="style1">Author:</span></label></td>
    <td>
      <input name="txtAuthor" type="text" id="txtAuthor" size="50" maxlength="50" value="<%=author%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtPublisher"><span class="style1">Publisher:</span></label></td>
    <td><input name="txtPublisher" type="text" size="50" maxlength="50" value="<%=publisher%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtPrice" class="style1">Price:</label></td>
    <td><input name="txtPrice" type="text" size="50" maxlength="50" value="<%=price%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtGender" class="style1">Genre:</label></td>
    <td>
    <span class="style1">
    <select name="txtGender">
    <option selected>
    <option value="Multi-Agent">Multi-Agent
    <option value="Fiction">Fiction
    <option value="Biography">Biography
    </td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtImage" class="style1">Image:</label></td>
    <td><input name="txtImage" type="text" size="50" maxlength="50" value="<%=image%>" /></td>
  </tr>
  <tr>
    <td align="center" valign="middle" colspan="2"><input name="sbmtBookRegister" type="submit" value="Register" /></td>
  </tr>
</table>
<span class="style1"><center><b><%=msg%></b></center></span>
</form>
</body>
</html>
