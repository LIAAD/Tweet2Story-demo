from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

import json

import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
 
import text2story as t2s

class Handler(RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))

        narrative = t2s.Narrative(lang=data['lang'],
                                  text=data['text'],
                                  publication_time=data['publication_time'])

        narrative.extract_actors(*data['actor_extraction_tools'])
        narrative.extract_times(*data['time_extraction_tools'])
        narrative.extract_events(*data['event_extraction_tools'])
        narrative.extract_objectal_links(*data['objectal_link_extraction_tools'])
        narrative.extract_semantic_role_links(*data['semantic_role_link_extraction_tools'])

        self.write(narrative.ISO_annotation())

if __name__ == '__main__':
    t2s.start()

    app = Application([
        (r"/", Handler)
    ])
    http_server = HTTPServer(app)
    http_server.listen(8888)

    print('Finished configuring')

    IOLoop.instance().start()
