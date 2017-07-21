def show(parameters):
    '''Advanced page for setting up things such as the encryption key'''
    from maintenance import maintenance
    
    maintenance()
    
    title = "Advanced"
    header = ""
    h1 = title
    body = '''Please do not make any changes unless technical support directs.
    <br />
    <form method='get' action='/advanced/save'>
    <table>
    <tr>
    <td>Encryption key:</td><td><input name='key1' type='password' /></td>
    </tr>
    <tr>
    <td>Repeat key:</td><td><input name='key2' type='password' /></td>
    </tr>
    <tr><td></td><td></td></tr>
    <tr><td></td><td><div align='right'><input type='submit' value='Next'>
    </div></td></tr>
    </form>'''
    return (title, header, h1, body)