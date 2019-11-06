<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<%

String userName = "guest";
if (session.getAttribute("username") != null) {
    userName = session.getAttribute("username").toString();
}

%>

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Menu</title>

<style type="text/css">
<!--
.style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt;
}
-->
<!--
.style2 {font-family: Copperplate Gothic Bold, Helvetica, sans-serif; font-size:16pt; color:#0000FF;
}
-->
</style>

</head>

<jsp:include page="header.jsp" />

<hr size=1>

<%

// show suggestions or search result

// if there is not a list of books in the session, get suggestions
if (session.getAttribute("books") == null) {
    Message m  = new Message("(askOne)");
    m.put("receiver", userName);
    m.put("content", "book_suggestion");

    Message answer = mbox.ask(m);

    System.out.println("suggestion answer = "+answer);
    ListTerm lbooks = ListTermImpl.parseList(answer.get("content").toString());
    session.setAttribute("books", lbooks);
}
%>

<jsp:include page="listBooks.jsp" />

<%
if (userName.equals("guest")) { 
%>
<hr>
<table border="0">
<tr>
<td>    
<form id="loginForm" name="loginForm" method="post" action="login.jsp">
    User: <input name="txtUser" type="text" id="txtUser" size="10" maxlength="10" />
    Password: <input name="txtPassword" type="password" id="txtPassword" size="10" maxlength="10"/>
    <input name="sbmtLogin" type="submit" id="Submit" value="Login" />	
</form>
</td>
<td>
<form method="post" action="registerUser.jsp">
    or
    <input name="sbmtLogin" type="submit" id="Submit" value="Register" />	
</form>
</td>
</tr>    
</table>
<%}%>


</body>
<hr size=1>
<a href="index.jsp"><center></b>Modules</center>
</span>
</html>

