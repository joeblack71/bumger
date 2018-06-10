from flask import (
	Blueprint, current_app, flash, g, json, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_weasyprint import render_pdf, HTML

#from flask_mail import Message

#from flasker.auth import login_required
from manager.db import get_db

#from manager import mail

import time
import locale

from num2words import num2words

bp = Blueprint('payment', __name__, url_prefix='/payment')

@bp.route('/')
def index():
    db = get_db()
    payments = db.execute(
            'SELECT p.id, o.prop_alias property, o.name as receiver_name,'
            '       c.description as concept,'
            '       r.number, r.amount, r.issue_date receipt_date, p.payment_date, p.amount, r.status'
            '  FROM payment p'
            '       LEFT JOIN receipt r ON p.receipt_id = r.id'
            '       LEFT JOIN concept c ON r.concept_id = c.id'
            '       LEFT JOIN occupant o ON r.person_id = o.id'
            ' WHERE r.status = "C"'
            ' ORDER BY p.payment_date DESC'
    ).fetchall()

    return render_template('payment/index.html', payments=payments)


@bp.route('/create', methods=('GET','POST'))
##@login_required
def create():
    if request.method == 'POST':
        receipt_id = request.form['receipt']
        amount = request.form['amount']
        payment_date = request.form['payment_date']
        note = request.form['payment_note']

        error = None

        if not receipt_id:
            error = 'Receipt number is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            ##c = db.cursor()
            payment_id = db.execute(
                'INSERT INTO payment (receipt_id, amount, payment_date)'
                ' VALUES (?, ?, ?)',
                (receipt_id, amount, payment_date)
            ).lastrowid
            ##payment_id = c.lastrowid
            db.commit()

            db.execute(
                'UPDATE receipt SET status = ?'
                ' WHERE id = ?',
                ('C', receipt_id)
            )
            db.commit()

            current_app.logger.debug('Payment note: ' + note)

            if note:
                db.execute(
                    'INSERT INTO payment_note (payment_id, text)'
                    ' VALUES (?, ?)',
                    (payment_id, note)
                )
                db.commit()

            return redirect(url_for('payment.index'))



    db = get_db()

    receipt_id = request.args.get('receipt_id')

    if not receipt_id:
        receipts = db.execute(
                'SELECT r.id, number, c.description, amount, r.status'
                ' FROM receipt r'
                '      JOIN concept c ON r.concept_id = c.id'
                ' ORDER BY number'
        ).fetchall()
    else:
        receipts = db.execute(
                'SELECT r.id, number, c.description, amount, r.status'
                ' FROM receipt r'
                '      JOIN concept c ON r.concept_id = c.id'
                ' WHERE r.id = ?',
                (receipt_id,)
        ).fetchall()

    receiver_id = request.args.get('receiver_id')

    if not receiver_id:
        receivers = db.execute(
                'SELECT id, name, property'
                ' FROM occupant o'
                ' ORDER BY name'
        ).fetchall()
    else:
        current_app.logger.debug('receiver_id: ' + str(receiver_id))

        receivers = db.execute(
                'SELECT id, name, property'
                ' FROM occupant'
                ' WHERE id = ?',
                (receiver_id,)
        ).fetchall()

    current_app.logger.debug('receivers: ' + str(len(receivers)))

    return render_template('payment/create.html', receipts=receipts, receivers=receivers)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
##@login_required
def update(id):
    if request.method == 'POST':
            amount = request.form['amount']
            payment_date = request.form['payment_date']
            status = request.form['status']
            error = None

            if not payment_date:
                error = 'Issue date is required.'

            if error is not None:
                    flash(error)
            else:
                    db = get_db()
                    db.execute(
                            'UPDATE payment SET payment_date = ?, amount = ?'
                            ' WHERE id = ?',
                            (payment_date, amount, id)
                    )
                    db.commit()
                    return redirect(url_for('payment.index'))

    db = get_db()

    payment = get_payment(id)

    receivers = db.execute(
            'SELECT id, name, prop_alias'
            ' FROM occupant'
            ' ORDER BY name'
    ).fetchall()

    concepts = db.execute(
            'SELECT id, description'
            ' FROM concept'
            ' ORDER BY id'
    ).fetchall()
    #' WHERE status = 1'

    return render_template('payment/update.html', payment=payment, receivers=receivers, concepts=concepts)


def get_payment(id, check_user=True):
    payment = get_db().execute(
            'SELECT py.id, py.amount, py.payment_date,'
                  ' c.id as concept_id, c.description as concept_desc,'
                  ' o.id receiver_id, o.name as receiver_name, o.property,'
                  ' r.id as receipt_id, r.number receipt_number, r.amount receipt_amount,'
                  ' r.issue_date as receipt_date, r.status'
            '  FROM payment py'
                  ' LEFT JOIN receipt r ON py.receipt_id = r.id'
                  ' LEFT JOIN concept c ON r.concept_id = c.id'
                  ' LEFT JOIN occupant o ON r.person_id = o.id'
            ' WHERE py.id = ?',
            (id,)
    ).fetchone()

    if payment is None:
        abort(404, "Receipt id {0} does not exist.".format(id))

    return payment


@bp.route('/_receiver_receipts', methods=['GET','POST'])
def populate_receipts():
    person_id = request.args.get('person_id', 0);

    current_app.logger.debug('person_id: ' + person_id)

    receipts = get_db().execute(
        'SELECT r.id, number || " - " || c.description as concept'
        '  FROM receipt r'
        '       JOIN concept c ON r.concept_id = c.id'
        ' WHERE r.person_id = ?',
        (person_id,)
    ).fetchall()

    current_app.logger.debug('found receipts: ' + str(len(receipts)))

    #dict_receipts = [dict(rec) for rec in receipts]

    return jsonify(result=[dict(rec) for rec in receipts])
"""
    receipts_as_dict = []

    for receipt in receipts:
        receipt_as_dict = {
            'id' : receipt.id,
            'number' : receipt.number}
        receipts_as_dict.append(receipt_as_dict)
"""

@bp.route('/<int:id>/payment_pdf')
def prepare_receipt(id):
    receipt = get_pdf_receipt(id)

    loc = locale.setlocale(locale.LC_ALL,'es_PE.utf8')
    current_app.logger.debug(loc)

    today = time.strftime("%d de %B del %Y")
    amount_text = num2words(receipt['amount'], lang='es').title()
    rec_form = {'str_amount': amount_text,
                'city': 'Santiago de Surco',
                'today': today}

    ##current_app.logger.debug(receipt.number)

    html = render_template('payment/receipt.html', receipt=receipt, rec_form=rec_form)

    return render_pdf(HTML(string=html))

def get_pdf_receipt(id):
    receipt = get_db().execute(
            'SELECT r.id, number, c.description as concept,'
                  ' p.first_name || " " || p.last_name as owner,'
                  ' pr.description as property, pm.amount, payment_date,'
                  ' pn.text as note, r.status'
            '  FROM receipt r'
                  ' LEFT JOIN person p ON r.person_id = p.id'
                  ' LEFT JOIN owner o ON r.person_id = o.person_id'
                  ' LEFT JOIN tenant t ON r.person_id = t.person_id'
                  ' LEFT JOIN property pr ON ( o.property_id = pr.id OR t.property_id = pr.id )'
                  ' LEFT JOIN concept c ON r.concept_id = c.id'
                  ' LEFT JOIN payment pm ON r.id = pm.receipt_id'
                  ' LEFT JOIN payment_note pn ON pm.id = pn.payment_id'
            ' WHERE r.id = ?',
            (id,)
    ).fetchone()

    current_app.logger.debug(receipt)

    if receipt is None:
        abort(404, "Receipt id {0} does not exist.".format(id))

    return receipt

@bp.route('/<int:id>/delete', methods=('POST',))
##@login_required
def delete(id):
    ##payment = get_payment(id)
    db = get_db()
    db.execute('DELETE FROM payment WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('payment.index'))


"""
@bp.route('/<int:id>/email')
def send_email(id):
    payment = get_payment(id)

    msg = Message("Hello",
                  sender="jolivas71@gmail.com",
                  recipients=["jolivas71@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"

    #mail.send(msg)

    return redirect('/')
"""
