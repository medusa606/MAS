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
<title>Register problem</title>
</head>
<a href="menu.jsp?codeUserURL=<%= request.getParameter("codeClient") %>"><img src="image/Cabecalho.jpg"></a>
<body>

<%
String      codeClient  = request.getParameter("codeClient"); 
String      codePurc    = request.getParameter("codePurc");
String      name        = request.getParameter("name");
String      titleBook   = request.getParameter("titleBook");
String      msg         = "";

if (request.getParameter("problem") != null) {
    String  problem = request.getParameter("problem");
   
    if (! problem.equals("")){
        Message m = new Message("(ask :receiver deliveryManager)");
        Literal c = Literal.parseLiteral("registerProblem("+codePurc+",\""+problem+"\")");
        m.put("content", c);
        Message r = mbox.ask(m);
        msg       = r.get("content").toString().replaceAll("\"","");
    }
}

%>

<form id="confirmBuy" name="confirmBuy" method="post" action="">
<h2 align="center"><span class="style2">Register problem</h2>
    <table  width="900" border="0">
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Code purchase:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= codePurc %></span></b></label>
            </td>
        </tr>
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Title:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= titleBook %></span></b></label>
            </td>
        </tr>
        <tr>
            <td width="450" align="right" valign="middle"><label for="textfield"><span class="style1">Name:</span></label>
            </td>
            <td width="450" align="left" valign="middle"><label for="textfield"><b><span class="style1"><%= name %></span></b></label>
            </td>
        </tr>
    </table>
    
    <p>
    <table  width="980" border="0">
         <tr>
            <td width="980" align="center" valign="middle">
            <span class="style1">
            Please, write your problem:<br>
            <textarea name="problem" name="problem" rows="3" cols="40"></textarea>
            </span>
            </td>
        </tr>
         <tr>
            <td width="980" align="center" valign="middle">
                <input name="sbmtProblem" type="submit" value="Register"/>
                <p>
                <b><span class="style1"><%=msg%></span></b>
            </td>
        </tr>
    </table>
</form>

</body>
</html>