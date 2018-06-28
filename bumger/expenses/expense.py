from flask import (
	Blueprint, flash, g, json, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flask_weasyprint import render_pdf, HTML

#from flask_mail import Message

#from flasker.auth import login_required
from ..db import get_db

from flask import current_app

bp = Blueprint('expense', __name__, url_prefix='/expenses')

@bp.route('/')
def index():
    db = get_db()
    expenses = db.execute(
        'SELECT e.id, e.expense_date, e.bill_number, e.amount,'
        '       p.first_name as provider_name, pr.description as concept'
        ' FROM expense e'
        '      JOIN person p on e.provider_id = p.id'
        '      JOIN product pr on e.product_id = pr.id'
        ' ORDER BY expense_date DESC'
    ).fetchall()

    return render_template('expense/index.html', expenses=expenses)

@bp.route('/create', methods=('GET','POST'))
##@login_required
def create():
    if request.method == 'POST':
        bill_number = request.form['bill_number']
        provider_id = request.form['provider']
        product_id = request.form['concept']
        ##quantity = request.form['quantity']
        amount = request.form['amount']
        expense_date = request.form['expense_date']

        error = None

        if not provider_id:
            error = 'Provider is required.'

        if not bill_number:
            error = 'Receipt number is required.'

        if not product_id:
            error = 'Product is required.'

        if not amount:
            error = 'Amount is required.'

        if not expense_date:
            error = 'Expense date is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO expense (provider_id, bill_number, product_id, amount, expense_date)'
                ' VALUES (?, ?, ?, ?, ?)',
                (provider_id, bill_number, product_id, amount, expense_date)
            )
            db.commit()
            return redirect(url_for('expense.index'))

    db = get_db()
    providers = db.execute(
            'SELECT id, name'
            ' FROM provider'
            ' ORDER BY name'
    ).fetchall()

    concepts = db.execute(
            'SELECT id, description'
            ' FROM product'
            ' ORDER BY description'
    ).fetchall()

    return render_template('expense/create.html', providers=providers, concepts=concepts)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
##@login_required
def update(id):
    expense = get_expense(id)

    if request.method == 'POST':
            issue_date = request.form['issue_date']
            status = request.form['status']
            error = None

            if not issue_date:
                error = 'Issue date is required.'

            if error is not None:
                    flash(error)
            else:
                    db = get_db()
                    db.execute(
                            'UPDATE expense SET issue_date = ?, status = ?'
                            ' WHERE id = ?',
                            (issue_date, status, id)
                    )
                    db.commit()
                    return redirect(url_for('expense.index'))

    db = get_db()
    providers = db.execute(
            'SELECT id, name'
            ' FROM provider'
            ' ORDER BY name'
    ).fetchall()

    products = db.execute(
            'SELECT id, description'
            ' FROM product'
            ' ORDER BY description'
    ).fetchall()

    return render_template('expense/update.html', expense=expense, owners=owners, concepts=concepts)

def get_expense(id, check_user=True):
    expense = get_db().execute(
            'SELECT e.id, e.bill_number, p.first_name as provider,'
                  ' pr.description as product_desc, e.amount, e.expense_date, e.status'
            '  FROM expense e'
                  ' JOIN person p on e.person_id = p.id'
                  ' JOIN product pr on e.product_id = pr.id'
            ' WHERE r.id = ?',
            (id,)
    ).fetchone()

    if expense is None:
        abort(404, "Receipt id {0} does not exist.".format(id))

    return expense

"""
@bp.route('/<int:id>/delete', methods=('POST',))
##@login_required
def delete(id):
    ##expense = get_expense(id)
    db = get_db()
    db.execute('DELETE FROM expense WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('expense.index'))
"""
