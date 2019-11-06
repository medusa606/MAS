
<!-- list book in the ListTerm stored in the session attibute "books" -->


<%@page contentType="text/html"%>
<%@page pageEncoding="UTF-8"%>
<%@page import="java.util.*"%>    
<%@page import="saci.*"%>   
<%@page import="jason.asSyntax.*"%>

<jsp:useBean id="mbox"  scope="application" class="saci.MBoxSAg" />

<table border="0">

<%

// show suggestions

ListTerm lbooks   = (ListTerm)session.getAttribute("books");
if (lbooks != null) {
    
if (lbooks.isEmpty()) {
    out.println("No books found!");
} 
for (Term tbc: lbooks) {
    Message m = new Message("(askOne :receiver stockManager)");
    Literal  cont = Literal.parseLiteral("book("+tbc+",B)");
    m.put("content", cont);
    Message answer = mbox.ask(m);
    Structure sa = (Structure)Structure.parse(answer.get("content").toString()).getTerm(1);
    // book(Code, Title, Authors, Publisher, Year, Genders, Price, Image, Weight)
    
    String  codeBook    =   sa.getTerm(0).toString();
    String  title       =   sa.getTerm(1).toString().replaceAll("\"","");
    String  publisher   =   sa.getTerm(3).toString().replaceAll("\"","");
    String  year        =   sa.getTerm(4).toString();
    String  price       =   sa.getTerm(6).toString();
    String  image       =   "image/" + sa.getTerm(7).toString().replaceAll("\"","");

    StringBuilder authorStr = new StringBuilder();
    ListTerm la = (ListTerm)sa.getTerm(2);
    if (la.size() == 1) {
        authorStr.append("Author: ");
    } else if (la.size() > 1) {
        authorStr.append("Authors: ");
    }

    Iterator<Term> ia = la.iterator();
    while (ia.hasNext()) {
        StringTerm a = (StringTerm)ia.next();
        authorStr.append(a.getString());
        if (ia.hasNext()) {
            authorStr.append(", ");
        }
    }
%>
<tr>
    <td>
        <img src="<%= image %>" /> 
    </td>
    <td>
        Title: <b>      <%= title %>   </b><br>
        <%= authorStr %>      <br>
        Publisher:  <%= publisher %>, <%= year %><br>
        Price: $  <b>   <%= price %>   </b><br>
    
        <button value="Buy" type="button" onclick="JavaScript: window.location.href = 'buyBook.jsp?bookId=<%= codeBook %>';">Buy</button>
    </td>
    </tr>
<%
} // end for
} // enf if
%>
</table>

