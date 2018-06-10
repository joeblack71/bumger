from flask import (
	Blueprint, current_app, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

##from flask_weasyprint import render_pdf, HTML

##from flask_mail import Message

#from flasker.auth import login_required
from manager.db import get_db

#from manager import mail
from datetime import datetime

bp = Blueprint('receipt', __name__, url_prefix='/receipt')

@bp.route('/')
def index():
    db = get_db()
    receipts = db.execute(
		'SELECT r.id, o.id as receiver_id,'
        '       o.name as receiver, o.prop_alias as property,'
        '       r.number, c.description concept, r.amount, r.issue_date, r.status'
        ' FROM receipt r'
        '       LEFT JOIN occupant o ON r.person_id = o.id'
        '       LEFT JOIN concept c ON r.concept_id = c.id'
        ' ORDER BY issue_date DESC'
	).fetchall()

    current_app.logger.debug('receipts counter: ' + str(len(receipts)))

    return render_template('receipt/index.html', receipts=receipts)

@bp.route('/create', methods=('GET','POST'))
##@login_required
def create():
    if request.method == 'POST':
        number = request.form['number']
        concept = request.form['concept']
        receiver = request.form['receiver']
        amount = request.form['amount']
        issue_date = request.form['issue_date']
        status = request.form['status']
        error = None

        if not number:
            error = 'Receipt number is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO receipt (number, concept_id, person_id, amount, issue_date, status)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (number, concept, receiver, amount, issue_date, status)
            )
            db.commit()
            return redirect(url_for('receipt.index'))

    db = get_db()
    receivers = db.execute(
            'SELECT *'
            ' FROM occupant'
            ' ORDER BY name'
    ).fetchall()

    concepts = db.execute(
            'SELECT id, description'
            ' FROM concept'
            ' ORDER BY id'
    ).fetchall()

    current_app.logger.debug('found concepts: ' + str(len(receivers)))

    return render_template('receipt/create.html', receivers=receivers, concepts=concepts)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
##@login_required
def update(id):
    if request.method == 'POST':
            ##issue_date = datetime.strptime(request.form['issue_date'], '%d/%m/%Y')
            issue_date = request.form['issue_date']
            ##iss_date = datetime.strptime(issue_date, '%d/%m/%Y')
            status = request.form['status']
            error = None

            if not issue_date:
                error = 'Issue date is required.'

            if error is not None:
                    flash(error)
            else:
                db = get_db()

                db.execute(
                        'UPDATE receipt SET issue_date = ?, status = ?'
                        ' WHERE id = ?',
                        (issue_date, status, id)
                )

                db.commit()

                return redirect(url_for('receipt.index'))

    db = get_db()

    receipt = get_receipt(id)

    receivers = db.execute(
            'SELECT id, prop_alias, name'
            ' FROM occupant'
            ' ORDER BY name'
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


def get_receipt(id, check_user=True):
    receipt = get_db().execute(
            'SELECT r.id, number, c.id as concept_id, c.description as concept_desc,'
                  ' p.id as receiver_id, p.first_name || " " || p.last_name as receiver,'
                  ' pr.description, amount, issue_date, r.status'
            '  FROM receipt r'
                  ' JOIN person p on r.person_id = p.id'
                  ' JOIN owner o on r.person_id = o.person_id'
                  ' JOIN property pr on o.property_id = pr.id'
                  ' JOIN concept c on r.concept_id = c.id'
            ' WHERE r.id = ?',
            (id,)
    ).fetchone()

    if receipt is None:
        abort(404, "Receipt id {0} does not exist.".format(id))

    return receipt
