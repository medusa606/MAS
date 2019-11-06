<!-- create the page header for some user -->

<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<%
String  userName    = session.getAttribute("username").toString();
String  msgWelcome  = "Welcome Guest";
if (!userName.equals("guest")) {
    msgWelcome = "Welcome "+session.getAttribute("name");
}
%>

<img src="image/Cabecalho.jpg">

<hr size=1>

<form id="searchForm" name="searchForm" method="post" action="search.jsp">
    <font color="#000000"><b><%=msgWelcome%></b> -- </font>

    <input name="key" type="text" id="txtUser" size="20" />
    <input  type="submit" id="Submit" value="Search" />	

<% if (!userName.equals("guest")) { %>
   <!--a href="orders.jsp">Orders</a> | -->
   <a href="logout.jsp">Logout
<%}%>

</form>

