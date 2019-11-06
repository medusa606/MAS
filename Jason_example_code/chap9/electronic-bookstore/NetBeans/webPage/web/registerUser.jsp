<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>

<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<%!

private String getPar(HttpServletRequest request, String par) {
    String s = request.getParameter(par);
    if (s == null) return "";
    return s;
}

%>

<%
String aux     = "";
String msg     = ""; 
String name    = getPar(request, "txtName");
String address = getPar(request, "txtAddress");
String uptown  = getPar(request, "txtUptown");
String city    = getPar(request, "txtCity");
String zipCode = getPar(request, "txtZipCode");
String state   = getPar(request, "txtState");
String phone   = getPar(request, "txtPhone");
String email   = getPar(request, "txtEMail");
String username= getPar(request, "txtUsername");
String password= getPar(request, "txtPassword");
String confirmPassword = getPar(request, "txtConfirmPassword");
    
if (name.length() > 0 && username.length() > 0) {
    if  ((confirmPassword.equals(password)) && (! name.equals("")))  {
        Message m = new Message("(askOne :receiver login)");
        m.put("content", "add_client("+username+",\""+password+"\",\""+name+"\",\""+address+"\",\""+uptown+"\",\""+city+"\",\""+zipCode+"\",\""+state+"\",\""+phone+"\",\""+email+"\")");
        Message r = mbox.ask(m);
        if (!r.get("content").toString().startsWith("ok")) {
            msg = r.get("content").toString();
        } else {
            session.setAttribute("username",username);
            session.setAttribute("password",password);
            %>
            <jsp:forward page="login.jsp" />
            <%
        }
    } else {
        msg += "The passwords does not match!<br>";
    }
} else {
    msg = "Name and username must be filled.";
}

%>

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>New User register</title>
<style type="text/css">
<!--
.style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt}
-->
<!--
.style2 {font-family: Arial, Helvetica, sans-serif; font-size:15pt}
-->
</style>

</head>
<img src="image/Cabecalho.jpg"></a>
<body>
<h1 align="center"><span class="style2">New User register</h1>

<form id="userRegisterForm" name="userRegisterForm" method="post" action="">
<table  border="0" align="center">
  <tr>
    <td width="90" align="right" valign="middle"><label for="txtName"><span class="style1">Name (*):</span></label></td>
    <td width="354">
      <input name="txtName" type="text" id="txtName" size="50" maxlength="50" value="<%=name%>" />    </td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtAddress"><span class="style1">Address:</span></label></td>
    <td>
      <input name="txtAddress" type="text" id="txtAddress" size="50" maxlength="50" value="<%=address%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtUptown"><span class="style1">Uptown:</span></label></td>
    <td><input name="txtUptown" type="text" size="50" maxlength="50" value="<%=uptown%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtCity" class="style1">City:</label></td>
    <td><input name="txtCity" type="text" size="50" maxlength="50" value="<%=city%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtZipCode" class="style1">Zip code:</label></td>
    <td><input name="txtZipCode" type="text" size="50" maxlength="50" value="<%=zipCode%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtState" class="style1">State:</label></td>
    <td><input name="txtState" type="text" size="50" maxlength="50" value="<%=state%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtPhone" class="style1">Phone:</label></td>
    <td><input name="txtPhone" type="text" size="50" maxlength="50" value="<%=phone%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtEMail" class="style1">EMail:</label></td>
    <td><input name="txtEMail" type="text" size="50" maxlength="50" value="<%=email%>" /></td>
  </tr>
   <tr>
    <td align="right" valign="middle"><label for="txtUsername" class="style1">Username (*):</label></td>
    <td><input name="txtUsername" type="text" size="12" maxlength="12" value="<%=username%>" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtPassword" class="style1">Password:</label></td>
    <td><input name="txtPassword" type="password" size="12" maxlength="12" value="" /></td>
  </tr>
  <tr>
    <td align="right" valign="middle"><label for="txtConfirmPassword" class="style1">Confirm:</label></td>
    <td><input name="txtConfirmPassword" type="password" size="12" maxlength="12" value="" /></td>
  </tr>
  <tr>
    <td align="center" valign="middle" colspan="2" height="50">
    <input name="sbmtUserRegister" type="submit" value="Register" />
    </td>
  </tr>
</table>
<p>
<font color="#FF0000"><center><%=msg%></center></font>
</form>
</body>

</html>
