from flask.views import MethodView
from flask import current_app, jsonify, abort
from flask_login import login_required, current_user
from . import api


class AccountView(MethodView):
    decorators = [login_required]

    def get(self, account_id):
        if account_id is None:
            # List all resources
            accounts = []
            for a in current_user.accounts:
                accounts.append({ 'id': a.number, 'number': a.number, 'balance': a.balance })
            return { 'data': accounts }
        else:
            # Return specific resource
            return jsonify({'single': 'value'})


    def post(self):
        pass  # Create new resource

    def delete(self, user_id):
        pass  # Delete resource

    def put(self, user_id):
        pass  # Update resource


account_view = AccountView.as_view('accounts')
api.add_url_rule('/accounts/', defaults={'account_id': None},
                 view_func=account_view, methods=['GET'])
api.add_url_rule('/accounts/', view_func=account_view, methods=['POST'])
api.add_url_rule('/accounts/<int:user_id>', view_func=account_view, methods=['GET', 'PUT', 'DELETE'])





class StockView(MethodView):
    def get(self, stock_id):
        if stock_id is None:
            pass  # List all resources
        else:
            pass  # Return specific resource


    # def post(self):
    #     # Should probably not be allowed for this resource
    #     pass  # Create new resource
    #
    #
    # def delete(self, stock_id):
    #     # Should probably not be allowed
    #     pass  # Delete resource
    #
    #
    # def put(self, stock_id):
    #     # Should probably not be allowed
    #     pass  # Update resource


stock_view = StockView.as_view('stock_view')
api.add_url_rule('/stocks/', defaults={'stock_id': None},
                 view_func=stock_view, methods=['GET'])
api.add_url_rule('/stocks/<string:stock_id>', view_func=stock_view, methods=['GET'])


# @api.route('/')
# def index():
#     """Default application route."""
#     msg = {'message': 'Welcome to Bank of Evil.'}
#     resp = jsonify(msg)
#     resp.status_code = 200
#     return resp
#
#
# @auth_required
# @api.route('/accounts', methods=['GET', 'POST'])
# def create_accounts():
#     return
