from flask import (
	Blueprint, current_app, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from datetime import datetime

#from flasker.auth import login_required
from ..db import get_db

bp = Blueprint('receipt', __name__)

@bp.route('/')
def index():
    db = get_db()
    receipts = db.execute(
		'SELECT r.id, po.occupant_id as receiver_id,'
        '       po.occupant_name as receiver, po.property_alias as property,'
        '       r.number, c.description concept, r.amount, r.issue_date, r.status'
        ' FROM receipt r'
        '       LEFT JOIN property_occupant po ON r.person_id = po.occupant_id'
        '       LEFT JOIN concept c ON r.concept_id = c.id'
        ' ORDER BY issue_date DESC'
	).fetchall()

    current_app.logger.debug('receipts counter: ' + str(len(receipts)))

    return render_template('receipt/index.html', receipts=receipts)

@bp.route('/create', methods=('GET','POST'))
##@login_required
def create():
    if request.method == 'POST':
        receipt_number = request.form['number']
        concept_id = request.form['concept']
        receiver_id = request.form['receiver']
        amount = request.form['amount']
        ##issue_date = datetime.strptime(request.form['issue_date'], '%d/%m/%Y')
        issue_date = request.form['issue_date']

        error = None

        if not receipt_number:
            error = 'Receipt number is required.'
        elif not concept_id:
            error = 'Concept is required.'
        elif not receiver_id:
            error = 'Receiver is required.'
        elif not amount:
            error = 'Amount is required.'
        elif not issue_date:
            error = 'Issue date is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO receipt (number, concept_id, person_id, amount, issue_date)'
                ' VALUES (?, ?, ?, ?, ?)',
                (receipt_number, concept_id, receiver_id, amount, issue_date)
            )
            db.commit()
            return redirect(url_for('receipt.index'))

    db = get_db()
    receivers = db.execute(
            'SELECT occupant_id as receiver_id, occupant_name as receiver_name,'
            ' property_id, property_description, property_alias'
            ' FROM property_occupant'
            ' ORDER BY occupant_name'
    ).fetchall()

    concepts = db.execute(
            'SELECT id, description'
            ' FROM concept'
            ' ORDER BY id'
    ).fetchall()

    return render_template('receipt/create.html', receivers=receivers, concepts=concepts)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
##@login_required
def update(id):
    if request.method == 'POST':
        receipt_number = request.form['number']
        concept_id = request.form['concept']
        receiver_id = request.form['receiver']
        amount = request.form['amount']
        ##issue_date = datetime.strptime(request.form['issue_date'], '%d/%m/%Y')
        issue_date = request.form['issue_date']
        status = request.form['status']

        error = None

        if not receipt_number:
            error = 'Receipt number is required.'
        if not concept_id:
            error = 'Concept is required.'
        if not receiver_id:
            error = 'Receiver is required.'
        if not amount:
            error = 'Amount is required.'
        if not issue_date:
            error = 'Issue date is required.'

        if error is not None:
                flash(error)
        else:
            db = get_db()

            db.execute(
                    'UPDATE receipt SET number=?, concept_id=?,'
                    ' person_id=?, amount=?, issue_date=?, status=?'
                    ' WHERE id=?',
                    (receipt_number, concept_id, receiver_id, amount, issue_date, status, id)
            )

            db.commit()

            return redirect(url_for('receipt.index'))

    db = get_db()

    receipt = get_receipt(id)

    receivers = db.execute(
            'SELECT occupant_id as receiver_id, occupant_name as receiver_name,'
            ' property_id, property_description, property_alias'
            ' FROM property_occupant'
            ' ORDER BY occupant_name'
    ).fetchall()


    concepts = db.execute(
            'SELECT id, description'
            ' FROM concept'
            #' WHERE status = 1'
            ' ORDER BY id'
    ).fetchall()

    return render_template('receipt/update.html', receipt=receipt, receivers=receivers, concepts=concepts)


@bp.route('/<int:id>/delete', methods=('POST',))
##@login_required
def delete(id):
    receipt = get_receipt(id)

    db = get_db()

    db.execute('DELETE FROM receipt WHERE id = ?', (id,))

    db.commit()

    return redirect(url_for('receipt.index'))


def get_receipt(id, check_user=False):
    receipt = get_db().execute(
    'SELECT r.id, number,'
    '       c.id as concept_id, c.description as concept_desc,'
    '       po.occupant_id as receiver_id, po.occupant_name as receiver_name,'
    '       po.property_id, po.property_alias,'
    '       amount, issue_date, r.status'
    '  FROM receipt r'
    '       LEFT JOIN property_occupant po on r.person_id = po.occupant_id'
    '       LEFT JOIN concept c on r.concept_id = c.id'
    ' WHERE r.id = ?;',
            (id,)
    ).fetchone()

    if receipt is None:
        abort(404, "Receipt id {0} does not exist.".format(id))

    return receipt
