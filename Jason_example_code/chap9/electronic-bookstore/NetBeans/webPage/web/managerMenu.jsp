<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Module Manager</title>
        
<style type="text/css">
<!--
.style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt}
-->
</style>
   
<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />


<img src="image/CabecalhoManager.jpg">
<hr size=2>       
</head>
    <body>
    <span class="style1">

        <h1>This options are not implemented yet!</h1>
        
    <form id="menuOptions" name="menuOptions" method="post" action="">
        <table width="980" border="0">
        
        <tr>
        <td width="980" height="35" align="center" scope="col">
        </tr>

        <tr>
        <td width="980" height="35" align="center" scope="col">
        <button align="center" value="RegisterBook" type="button" onclick="JavaScript: window.location.href = 'bookRegister.jsp';">Register book</button></td>
        </tr>
     
        <tr>
        <td width="980" height="35" align="center" scope="col">
        <button align="center" value="purchase" type="button" onclick="JavaScript: window.location.href = 'consultPurchase.jsp';">Purchase</button></td>
        </tr>

        <tr>
        <td width="980" height="35" align="center" scope="col">
        <button align="center" value="listBook" type="button" onclick="JavaScript: window.location.href = 'listBooks.jsp';">List of books</button></td>
        </tr>
        
        <tr>
        <td width="980" height="35" align="center" scope="col">
        <button align="center" value="listClient" type="button" onclick="JavaScript: window.location.href = 'listClients.jsp';">List of customers</button></td>
        </tr>

        <tr>
        <td width="980" height="35" align="center" scope="col">
        <button align="center" value="consultStock" type="button" onclick="JavaScript: window.location.href = 'stockBook.jsp';">Consult stock</button></td>
        </tr>
        
        <tr>
        <td width="980" height="35" align="center" scope="col">
        <button align="center" value="competitivePrice" type="button" onclick="JavaScript: window.location.href = 'competitivePrice.jsp';">Competitive price</button></td>
        </tr>
        
        <tr>
        <td width="980" height="35" align="center" scope="col">
        <button align="center" value="sendEmailFor" type="button" onclick="JavaScript: window.location.href = 'sendMail.jsp';">Send mail</button></td>
        </tr>
       
        <tr>
        <td width="980" height="35" align="center" scope="col">
        </tr>

        </table>
    </form>
    
    </body>
    <hr size=2>
    <a href="index.jsp"><center>Modules</center>
    </tr>
    </span>
</html>
