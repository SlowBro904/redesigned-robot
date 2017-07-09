def show(parameters):
    """Error log"""
    from errors import ERRORS
    from maintenance import maintenance
    
    maintenance()
    
    errors = ERRORS()
    
    title = "Error log"
    header = ""
    h1 = title
    
    body = "<table>"
    
    # FIXME Also capture hard errors
    for warning in errors.warnings:
        body += "<tr><td>" + warning + "</td></tr>"
    
    body += """</table><br />
    <br />
    <a href='/'>Home</a>"""
    
    return (title, header, h1, body)