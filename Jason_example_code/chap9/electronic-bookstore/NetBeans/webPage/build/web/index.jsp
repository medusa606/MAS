<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<%!
saci.MBoxSAg mbox;

public void jspInit() {

    System.out.println("Start page");
    Config c = new Config();
    c.set("society.name", "electronic_bookstore");
    try {
        mbox = new MBoxSAg("web",c);
        mbox.init();
        System.out.println("MBox created!");
        getServletContext().setAttribute("mbox", mbox);
    } catch (Exception e) {
        System.err.println("Error jsp "+e);
    }
}
%>

<%
// test 
    try {
        mbox = (saci.MBoxSAg)getServletContext().getAttribute("mbox");
        mbox.sendMsg(new Message("(tell :receiver login :content test)"));
    } catch (Exception e) {
        jspInit();
    }
    
    session.setAttribute("username","guest");
    session.removeAttribute("books");
%>

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
        <title>AgentSpeak(L) / Jason</title>
    </head>
    <body>

    <h1><span class="style2">Eletronic Bookstore modules</h1>
    
    <p><a href="userPage.jsp"><span class="style1">Client<br>
    <a href="managerMenu.jsp"><span class="style1">Manager</p>
   
    </span>
    </body>
</html>
