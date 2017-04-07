from flask import request, Response, render_template


class JSONResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
        if isinstance(rv, dict) and best == 'text/html' and request.accept_mimetypes[best] > request.accept_mimetypes['application/json']:
            rv = render_template('api/json.html', json=rv)
        return super(JSONResponse, cls).force_type(rv, environ)
