from flask import Blueprint, request, jsonify, render_template
from .models import Account
from . import db
from .schemas import account_schema, accounts_schema
from datetime import datetime

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/accounts', methods=['POST'])
def create_account():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    # validate
    errors = account_schema.validate(json_data)
    if errors:
        return jsonify(errors), 400

    # check unique email
    if Account.query.filter_by(email=json_data['email']).first():
        return jsonify({"message": "Email already exists"}), 400

    # parse date
    dob = datetime.fromisoformat(json_data['dob']).date()

    acc = Account(
        name=json_data['name'],
        email=json_data['email'],
        phone=json_data['phone'],
        dob=dob,
        balance=float(json_data.get('balance', 0.0))
    )
    db.session.add(acc)
    db.session.commit()
    return account_schema.jsonify(acc), 201

@bp.route('/api/accounts', methods=['GET'])
def list_accounts():
    accounts = Account.query.order_by(Account.created_at.desc()).all()
    return accounts_schema.jsonify(accounts)

@bp.route('/api/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    acc = Account.query.get_or_404(account_id)
    return account_schema.jsonify(acc)

