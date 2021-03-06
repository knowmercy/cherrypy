"""

Tutorial: HTTP errors

HTTPError is used to return an error response to the client.
CherryPy has lots of options regarding how such errors are
logged, displayed, and formatted.

"""

import cherrypy


class HTTPErrorDemo(object):
    
    def index(self):
        # display some links that will result in errors
        tracebacks = cherrypy.config.get('server.show_tracebacks')
        if tracebacks:
            trace = 'off'
        else:
            trace = 'on'
            
        return """
        <html><body>
            <h2><a href="toggleTracebacks">Toggle tracebacks %s</a></h2>
            <p><a href="/doesNotExist">Click me; I'm a broken link!</a></p>
            <p><a href="/error?code=403">Use a custom an error page from a file.</a></p>
            <p>These errors are explicitly raised by the application:</p>
            <ul>
                <li><a href="/error?code=400">400</a></li>
                <li><a href="/error?code=401">401</a></li>
                <li><a href="/error?code=402">402</a></li>
                <li><a href="/error?code=500">500</a></li>
            </ul>
            <p><a href="/messageArg">You can also set the response body
            when you raise an error.</a></p>
        </body></html>
        """ % trace
    index.exposed = True
    
    def toggleTracebacks(self):
        # simple function to toggle tracebacks on and off 
        tracebacks = cherrypy.config.get('server.show_tracebacks')
        cherrypy.config.update({'server.show_tracebacks': not tracebacks})
        
        # redirect back to the index
        raise cherrypy.HTTPRedirect('/')
    toggleTracebacks.exposed = True
    
    def error(self, code):
        # raise an error based on the get query
        raise cherrypy.HTTPError(status = code)
    error.exposed = True
    
    def messageArg(self):
        message = ("If you construct an HTTPError with a 'message' "
                   "argument, it wil be placed on the error page "
                   "(underneath the status line by default).")
        raise cherrypy.HTTPError(500, message=message)
    messageArg.exposed = True


cherrypy.root = HTTPErrorDemo()

# Set a custom response for 403 errors.
import os
localDir = os.path.dirname(__file__)
curpath = os.path.normpath(os.path.join(os.getcwd(), localDir))
cherrypy.config.update({'error_page.403' : os.path.join(curpath, "custom_error.html")})


if __name__ == '__main__':
    # Use the configuration file tutorial.conf.
    cherrypy.config.update(file = 'tutorial.conf')
    # Start the CherryPy server.
    cherrypy.server.start()
