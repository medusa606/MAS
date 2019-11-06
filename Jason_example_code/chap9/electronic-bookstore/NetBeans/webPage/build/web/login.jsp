<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<%
String msg = "";
String userName = "";
String password = "";

if (request.getParameter("txtUser") != null) {
    userName = request.getParameter("txtUser");
} else {
    userName = session.getAttribute("username").toString();
}


if (request.getParameter("txtPassword") != null) {
    password = request.getParameter("txtPassword");    
} else {
    password = session.getAttribute("password").toString();    
}

if  (userName.length() > 0 && password.length() > 0)  {
        Message m = new Message("(askOne :receiver login)");
        m.put("content", "user_logon("+userName+",\""+password+"\")");
        Message r = mbox.ask(m);
        
        String content = r.get("content").toString();
        if  (content.startsWith("client")) {
            Structure s = Structure.parse(content);
            String name = s.getTerm(0).toString().replaceAll("\"","");
            session.setAttribute("username",userName);
            session.setAttribute("name",name);
            %>
            <jsp:forward page="userPage.jsp" />
            <%
        } else {
            msg = "<b>"+r.get("content")+"</b><br/>";
        }
} else {
        msg = "<b>Empty password</b><br/>";
}


%>

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Login</title>

</head>
<img src="image/Cabecalho.jpg">

<hr>

<%=    msg %>

<hr>
<form id="loginForm" name="loginForm" method="post" action="login.jsp">
    User: <input name="txtUser" type="text" id="txtUser" size="10" maxlength="10" value="<%=userName%>"/>
    Password: <input name="txtPassword" type="password" id="txtPassword" size="10" maxlength="10" value="<%=password%>"/>
    <input name="sbmtLogin" type="submit" id="Submit" value="Login" />	
</form>

</body>
<hr size=1>
</html>

