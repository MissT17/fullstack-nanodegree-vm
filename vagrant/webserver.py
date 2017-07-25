from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from urlparse import urlparse

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Add a new restaurant to the database</a></br></br>"
                for item in list:
                    print item.id
                    output += item.name
                    output += "</br>"
                    output += "<a href='/%s/edit'>Update</a>" %item.id
                    output += "</br>"
                    output += "<a href='%s/delete'>Delete</a></br></br>"%item.id
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resto_id = self.path.split("/")[1]
                print resto_id
                delete_resto = session.query(Restaurant).filter_by(id = resto_id).first()
                output = ""
                output += "<html><body>"
                output += "Are you sure you would like to delete %s restaurant from the database" %delete_resto.name
                output += '''<form method='POST' enctype='multipart/form-data' action=''><input name="delete" type="submit" value= "Delete"></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a new restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newRestoName" type="text" placeholder='New Restaurant Name' ><input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                resto_id = self.path.split("/")[1]
                print resto_id
                resto_name = session.query(Restaurant.name).filter_by(id=resto_id).first()
                print resto_name
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit the information about the restaurant</h1>"
                output += "%s" %resto_name
                output += '''<form method='POST' enctype='multipart/form-data' action=''><input name="updated_info" type="text" ><input type="submit" value="Update"></form>''' 
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestoName')
                    new_resto = Restaurant(name=messagecontent[0])
                    session.add(new_resto)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    resto_id = self.path.split("/")[1]
                    delete_resto = session.query(Restaurant).filter_by(id=resto_id).one()
                    print delete_resto.name
                    print fields
                    if fields.get('delete')[0] == 'Delete':
                        session.delete(delete_resto)
                        session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(  
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_info = fields.get('updated_info')
                    print new_info
                    resto_id = self.path.split("/")[1]
                    print resto_id
                    resto_name = session.query(Restaurant).filter_by(id=resto_id).first()
                    resto_name.name = new_info[0]
                    session.add(resto_name)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()