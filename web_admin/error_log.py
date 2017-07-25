def show(parameters):
    '''Error log'''
    from os import dupterm
    from err import Err
    from maintenance import maint
    
    maint()
    
    err = Err()
    
    title = "Error log"
    
    # Zebra striped table
    header = '''<style>
    table {
        border-collapse: collapse;
        width: 100%;
    }

    th, td {
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even){background-color: #f2f2f2}
    </style>'''
    
    h1 = title
    
    body = "<table>"
    
    # TODO Paginate
    for log in err.log:
        body += "<tr><td>" + log + "</td></tr>"
    
    body += '''</table><br />
    <br />'''
    # FIXME Insert the console output here
    body += "<a href='/'>Home</a>"
    
    return (title, header, h1, body)