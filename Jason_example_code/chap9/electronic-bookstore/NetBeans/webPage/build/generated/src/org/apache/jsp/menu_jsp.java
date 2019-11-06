package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.util.*;
import saci.*;
import jason.asSyntax.*;

public final class menu_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static java.util.List _jspx_dependants;

  public Object getDependants() {
    return _jspx_dependants;
  }

  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws java.io.IOException, ServletException {

    JspFactory _jspxFactory = null;
    PageContext pageContext = null;
    HttpSession session = null;
    ServletContext application = null;
    ServletConfig config = null;
    JspWriter out = null;
    Object page = this;
    JspWriter _jspx_out = null;
    PageContext _jspx_page_context = null;


    try {
      _jspxFactory = JspFactory.getDefaultFactory();
      response.setContentType("text/html;charset=UTF-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\n");
      out.write("\n");
      out.write("    \n");
      out.write("   \n");
      out.write("\n");
      out.write("\n");
      saci.MBoxSAg mbox = null;
      synchronized (application) {
        mbox = (saci.MBoxSAg) _jspx_page_context.getAttribute("mbox", PageContext.APPLICATION_SCOPE);
        if (mbox == null){
          mbox = new saci.MBoxSAg();
          _jspx_page_context.setAttribute("mbox", mbox, PageContext.APPLICATION_SCOPE);
        }
      }
      out.write('\n');
      out.write('\n');


String  msgWelcome  = "Welcome Guest";
String  userName    = "";
String  password    = "";
String  name        = "";

if (session.getAttribute("username") != null) {
    userName = session.getAttribute("username").toString();
    name = session.getAttribute("name").toString();
}

if  ((request.getParameter("txtUser") != null) && 
    (request.getParameter("txtPassword") != null)) {
    
    userName    = request.getParameter("txtUser");
    password    = request.getParameter("txtPassword");
    
    if  (userName.length() > 0 && password.length() > 0)  {    
        Message m = new Message("(askOne :receiver salesAssistant)");
        Literal c = Literal.parseLiteral("user_logon(\""+userName+"\""+",\""+password+"\")");
        m.put("content", c);
        Message r = mbox.ask(m);
        
        Structure s = Structure.parse(r.get("content").toString());
        
        if  (!s.getFunctor().equals("error")) {
            name = s.getTerm(1).toString().replaceAll("\"","");
            msgWelcome  = "Welcome " + name;
            session.setAttribute("username",userName);
            session.setAttribute("name",name);
        }
    }
}


      out.write("\n");
      out.write("\n");
      out.write("<html xmlns=\"http://www.w3.org/1999/xhtml\">\n");
      out.write("<head>\n");
      out.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\" />\n");
      out.write("<title>Menu</title>\n");
      out.write("\n");
      out.write("<style type=\"text/css\">\n");
      out.write("<!--\n");
      out.write(".style1 {font-family: Arial, Helvetica, sans-serif; font-size:10pt;\n");
      out.write("}\n");
      out.write("-->\n");
      out.write("<!--\n");
      out.write(".style2 {font-family: Copperplate Gothic Bold, Helvetica, sans-serif; font-size:16pt; color:#0000FF;\n");
      out.write("}\n");
      out.write("-->\n");
      out.write("</style>\n");
      out.write("\n");
      out.write("</head>\n");
      out.write("<img src=\"image/Cabecalho.jpg\">\n");
      out.write("<body>\n");
      out.write("<span class=\"style1\">\n");
      out.write("\n");


// show suggestions

String msgGetBook   = "book_suggestion(guest,L)";
if  (userName.length() > 0)  {
     msgGetBook = "book_suggestion("+userName+",L)";
}

Message m  = new Message("(askOne :receiver salesAssistant)");
m.put("content", Literal.parseLiteral(msgGetBook));

Message answer = mbox.ask(m);
Structure sa   = Structure.parse(answerCB.get("content").toString());

for (Term tbc: (ListTerm)sa.getTerm(1)) {
    m = new Message("(askOne :receiver stockManager)");
    Literal  cont = Literal.parseLiteral("book("+tbc+")");
    m.put("content", cont);
    answer = mbox.ask(m);
    sa = Structure.parse(answer.get("content").toString());
    
    String  codeBook    =   sa.getTerm(0).toString();
    String  image       =   "image/" + sa.getTerm(1).toString().replaceAll("\"","");
    String  title       =   sa.getTerm(2).toString().replaceAll("\"","");
    String  author      =   sa.getTerm(3).toString().replaceAll("\"","");
    String  publisher   =   sa.getTerm(4).toString().replaceAll("\"","");
    String  price       =   sa.getTerm(5).toString();

      out.write("\n");
      out.write("    \n");
      out.write("    <img src=       ");
      out.print( image );
      out.write(">       <p>\n");
      out.write("    <b> Title:      ");
      out.print( title );
      out.write("        </b><br>\n");
      out.write("    <b> Author:     ");
      out.print( author );
      out.write("       </b><br>\n");
      out.write("    <b> Publisher:  ");
      out.print( publisher );
      out.write("    </b><br>\n");
      out.write("    <b> Price: $    ");
      out.print( price );
      out.write("        </b><br></p>\n");
      out.write("    \n");
      out.write("    <p><button value=\"Buy\" type=\"button\" onclick=\"JavaScript: window.location.href = 'buyBook.jsp?codeBook=");
      out.print( codeBook );
      out.write("';\">Buy</button></p>");

}

      out.write("\n");
      out.write("\n");
      out.write("<hr size=1>\n");
      out.write("\n");
      out.write("<form id=\"loginForm\" name=\"loginForm\" method=\"post\" action=\"\">\n");
      out.write("<font color=\"#000000\"><b><center>");
      out.print(msgWelcome);
      out.write("</center></b</font>\n");
      out.write("<hr size=2>\n");
      out.write("<table width=980 border=\"0\">\n");
      out.write("    <tr>\n");
      out.write("        <td width=\"162\" align=\"left\" scope=\"col\"><label for=\"textfield\"><span class=\"style1\">User:</span></label>\n");
      out.write("            <input name=\"txtUser\" type=\"text\" id=\"txtUser\" size=\"10\" maxlength=\"10\" value=\"");
      out.print( userName );
      out.write("\"/>\n");
      out.write("        </td>\n");
      out.write("            <td width=\"165\" align=\"left\" scope=\"col\"><label for=\"textfield\"><span class=\"style1\">Password:</span></label>\n");
      out.write("            <input name=\"txtPassword\" type=\"password\" id=\"txtPassword\" size=\"10\" maxlength=\"10\" value=\"");
      out.print( password );
      out.write("\"/>\n");
      out.write("        </td>\n");
      out.write("            <td width=\"30\" align=\"right\" scope=\"col\"><label for=\"Submit\"></label>\n");
      out.write("            <input name=\"sbmtLogin\" type=\"submit\" id=\"Submit\" value=\"Login\" />\t\n");
      out.write("        </td>\n");
      out.write("        <td width=\"400\" align=\"right\" scope=\"col\" class=\"style1\">\n");
      out.write("            <a href=\"search.jsp\">Search book\n");
      out.write("        </td>\n");
      out.write("        <td width=\"78\" align=\"right\" scope=\"col\" class=\"style1\">\n");
      out.write("            <a href=\"register.jsp\">Register\n");
      out.write("        </td>\n");
      out.write("        ");
 if (!userName.size() > 0) { 
      out.write("\n");
      out.write("        <td width=\"95\" align=\"right\" scope=\"col\" class=\"style1\">\n");
      out.write("            <a href=\"orders.jsp\">Orders\n");
      out.write("        </td>\n");
      out.write("        ");
}
      out.write("\n");
      out.write("    </tr>\n");
      out.write("</table>\n");
      out.write("</form>\n");
      out.write("\n");
      out.write("\n");
      out.write("</body>\n");
      out.write("<hr size=1>\n");
      out.write("<a href=\"index.jsp\"><center></b>Modules</center>\n");
      out.write("</span>\n");
      out.write("</html>\n");
      out.write("\n");
    } catch (Throwable t) {
      if (!(t instanceof SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          out.clearBuffer();
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
      }
    } finally {
      if (_jspxFactory != null) _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
