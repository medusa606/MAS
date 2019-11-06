<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<%
String key = request.getParameter("key");

if  (key != null && key.length() > 0) {
    String  userName = session.getAttribute("username").toString();
    
    Message m  = new Message("(askOne)");
    m.put("receiver", userName);
    m.put("content", "find_book(\""+key+"\",L)");
    Message answer = mbox.ask(m);

    Structure content = Structure.parse(answer.get("content").toString());
    ListTerm lbooks = (ListTerm)content.getTerm(1);
    session.setAttribute("books", lbooks);
}
%>

<jsp:forward page="userPage.jsp" />

