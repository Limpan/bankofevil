from flask import request, Response, render_template, make_response, jsonify
import simplejson as json

class JSONResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
            if best == 'text/html' and request.accept_mimetypes[best] > request.accept_mimetypes['application/json']:
                rv = make_response(render_template('api/json.html', response=json.dumps(rv, sort_keys=True, indent=2)))
            else:
                rv = jsonify(rv)
        return super(JSONResponse, cls).force_type(rv, environ)
