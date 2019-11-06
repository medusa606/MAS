package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import java.util.*;
import saci.*;
import jason.asSyntax.*;

public final class login_jsp extends org.apache.jasper.runtime.HttpJspBase
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
            
      out.write("\n");
      out.write("            ");
      if (true) {
        _jspx_page_context.forward("userPage.jsp");
        return;
      }
      out.write("\n");
      out.write("            ");

        } else {
            msg = "<b>"+r.get("content")+"</b><br/>";
        }
} else {
        msg = "<b>Empty password</b><br/>";
}



      out.write("\n");
      out.write("\n");
      out.write("<html xmlns=\"http://www.w3.org/1999/xhtml\">\n");
      out.write("<head>\n");
      out.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\" />\n");
      out.write("<title>Login</title>\n");
      out.write("\n");
      out.write("</head>\n");
      out.write("<img src=\"image/Cabecalho.jpg\">\n");
      out.write("\n");
      out.write("<hr>\n");
      out.write("\n");
      out.print(    msg );
      out.write("\n");
      out.write("\n");
      out.write("<hr>\n");
      out.write("<form id=\"loginForm\" name=\"loginForm\" method=\"post\" action=\"login.jsp\">\n");
      out.write("    User: <input name=\"txtUser\" type=\"text\" id=\"txtUser\" size=\"10\" maxlength=\"10\" value=\"");
      out.print(userName);
      out.write("\"/>\n");
      out.write("    Password: <input name=\"txtPassword\" type=\"password\" id=\"txtPassword\" size=\"10\" maxlength=\"10\" value=\"");
      out.print(password);
      out.write("\"/>\n");
      out.write("    <input name=\"sbmtLogin\" type=\"submit\" id=\"Submit\" value=\"Login\" />\t\n");
      out.write("</form>\n");
      out.write("\n");
      out.write("</body>\n");
      out.write("<hr size=1>\n");
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
