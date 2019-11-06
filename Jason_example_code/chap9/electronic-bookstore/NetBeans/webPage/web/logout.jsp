<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<%


if (session.getAttribute("username") != null) {
        String user = session.getAttribute("username").toString();
        session.setAttribute("username","guest");
        session.removeAttribute("books");

        Message m = new Message("(achieve :receiver login)");
        Literal c = Literal.parseLiteral("user_logout("+user+")");
        m.put("content", c);
        mbox.sendMsg(m);
}
%>

<jsp:forward page="userPage.jsp" />

</body>
</html>

