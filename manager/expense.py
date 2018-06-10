from flask import (
	Blueprint, flash, g, json, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

#from flask_weasyprint import render_pdf, HTML

#from flask_mail import Message

#from flasker.auth import login_required
from manager.db import get_db

#from manager import mail

from flask import current_app

bp = Blueprint('expense', __name__, url_prefix='/expense')

@bp.route('/')
def index():
    db = get_db()
    expenses = db.execute(
        'SELECT expense_date, receipt_number, amount, p.name as provider, pr.description as product'
        ' FROM expense e'
        '      JOIN provider p on e.provider_id = p.id'
        '      JOIN product pr on e.product_id = pr.id'
        ' ORDER BY expense_date DESC'
    ).fetchall()

    return render_template('expense/index.html', expenses=expenses)

@bp.route('/create', methods=('GET','POST'))
##@login_required
def create():
    if request.method == 'POST':
        provider_id = request.form['provider']
        product_id = request.form['product']
        quantity = request.form['quantity']
        amount = request.form['amount']
        expense_date = request.form['expense_date']

        error = None

        if not provider_id:
            error = 'Provider is required.'

        if not receipt:
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
                'INSERT INTO expense (provider_id, receipt_number, product_id, quantity, amount, expense_date)'
                ' VALUES (?, ?, ?, ?, ?)',
                (provider_id, receipt, product_id, quantity, amount, expense_date)
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

    return render_template('expense/create.html', providers=providers, products=products)

"""
@bp.route('/_owner_receipts', methods=['GET','POST'])
def populate_receipts():
    person_id = request.args.get('person_id', 0);

    current_app.logger.debug('person_id: ' + person_id)

    receipts = get_db().execute(
        'SELECT r.id, number || " - " || c.description as concept'
        '  FROM receipt r'
        '       JOIN concept c on r.concept_id = c.id'
        ' WHERE r.person_id = ?',
        (person_id,)
    ).fetchall()

    current_app.logger.debug('found receipts: ' + str(len(receipts)))

    #dict_receipts = [dict(rec) for rec in receipts]

    #current_app.logger.debug(str(dict_receipts[0]))

    return jsonify(result=[dict(rec) for rec in receipts])

def get_expense(id, check_user=True):
    expense = get_db().execute(
            'SELECT r.id, number, c.description as concept_desc, p.first_name as owner,'
                  ' pr.description, amount, issue_date, r.status'
            '  FROM expense r'
                  ' JOIN person p on r.person_id = p.id'
                  ' JOIN owner o on r.person_id = o.person_id'
                  ' JOIN property pr on o.property_id = pr.id'
                  ' JOIN concept c on r.concept_id = c.id'
            ' WHERE r.id = ?',
            (id,)
    ).fetchone()

    if expense is None:
        abort(404, "Receipt id {0} does not exist.".format(id))

    return expense

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
    owners = db.execute(
            'SELECT *'
            ' FROM person'
            ' ORDER BY first_name'
    ).fetchall()

    concepts = db.execute(
            'SELECT id, description'
            ' FROM concept'
            #' WHERE status = 1'
            ' ORDER BY id'
    ).fetchall()

    return render_template('expense/update.html', expense=expense, owners=owners, concepts=concepts)

@bp.route('/<int:id>/delete', methods=('POST',))
##@login_required
def delete(id):
    ##expense = get_expense(id)
    db = get_db()
    db.execute('DELETE FROM expense WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('expense.index'))

@bp.route('/<int:id>/expense_pdf')
def expense_pdf(id):
    expense = get_expense(id)
    rec_form = {'str_amount':'Doscientos Setentaicinco',
                'expense_month':'Mayo',
                'city':'Santiago de Surco',
                'day':'15',
                'expense_month':'Mayo',
                'year':'2018'}
    html = render_template('expense/expense.html',expense=expense, rec_form=rec_form)

    return render_pdf(HTML(string=html))
"""
