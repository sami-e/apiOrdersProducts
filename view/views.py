def index(data):
    view = f"""
    <html>
        <body>
            <h1>Hello World</h1> """
    view += f"""<p>{data}</p>"""
        
    view += """</body> </html> """
    return view
