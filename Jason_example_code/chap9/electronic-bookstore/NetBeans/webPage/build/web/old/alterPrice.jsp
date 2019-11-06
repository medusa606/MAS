<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Alter price</title>

<style type="text/css">
<!--
.style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt;
}
-->
<!--
.style2 {font-family: Arial, Helvetica, sans-serif; font-size:15pt}
-->
</style>

<html>
<head>

</head>
<a href="managerMenu.jsp"><img src="image/CabecalhoManager.jpg"></a>
<body>
<hr size=2>
<h2 align="center"><span class="style2">Alter price</h2>
<form id="searchForm" name="searchForm" method="post" action="">
<%

Message     msg;
Literal     cont;
Message     answer;
String      content, codeBookLis;
Term        terms;

codeBookLis = request.getParameter("codeBook");

if  (request.getParameter("price") != null) {
    String  newprice =   request.getParameter("price");   
    if  (! newprice.equals("")){
        msg         =   new Message("(ask :receiver stockManager)");
        cont        =   Literal.parseLiteral("alterPrice("+codeBookLis+","+newprice+")");
        msg.put("content", cont);
        answer      =   mbox.ask(msg);
        content     =   answer.get("content").toString();
     }
}

msg         =   new Message("(ask :receiver stockManager)");
cont        =   Literal.parseLiteral("showShopWindow("+codeBookLis+")");
msg.put("content", cont);
answer      =   mbox.ask(msg);
content     =   answer.get("content").toString();
    
terms       = Term.parse(content);
    
String  codeBook    =   terms.getTerm(0).toString().replaceAll("\"","");
String  image       =   "image/" + terms.getTerm(1).toString().replaceAll("\"","");
String  title       =   terms.getTerm(2).toString().replaceAll("\"","");
String  author      =   terms.getTerm(3).toString().replaceAll("\"","");
String  publisher   =   terms.getTerm(4).toString().replaceAll("\"","");
String  price       =   terms.getTerm(5).toString().replaceAll("\"",""); 
String  gender      =   terms.getTerm(6).toString().replaceAll("\"","");
    
if  (!title.equals("Book not found")) { %>
    <span class="style1">
    <img src=       <%= image %>>       <p>
    <font color="#FF0000">
    <b> Code:       <%= codeBook %>     </b><br></font>
    <b> Title:      <%= title %>        </b><br>
    <b> Author:     <%= author %>       </b><br>
    <b> Publisher:  <%= publisher %>    </b><br>
    <b> Price: $    <%= price %>        </b><br>
    <b> Genre:      <%= gender %>       </b><br></p>
        
    <input name="price" align="right" value="" type="text" id="price" size="10" maxlength="10" />
    <input name="sbmtStatus" type="submit" value="Confirm"/>

<%  }   %>

</form>
</body>
</span>
</html>
