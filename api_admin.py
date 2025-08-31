from flask import Blueprint, request, jsonify, current_app
from models import db, Scheme, SchemeTranslation
from datetime import datetime
import uuid

admin_bp = Blueprint('admin', __name__)

def gen_uuid():
    return str(uuid.uuid4())

@admin_bp.route('/schemes', methods=['POST'])
def create_scheme():
    data = request.json or {}
    # minimal validation
    code = data.get('code') or f"SCH_{uuid.uuid4().hex[:8]}"
    s = Scheme(
        code=code,
        category=data.get('category'),
        min_age=data.get('min_age'),
        max_age=data.get('max_age'),
        min_income=data.get('min_income'),
        max_income=data.get('max_income'),
        target_gender=data.get('target_gender'),
        states_applicable=data.get('states_applicable'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        official_url=data.get('official_url'),
        active=bool(data.get('active', True))
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id}), 201

@admin_bp.route('/schemes/<scheme_id>', methods=['PUT'])
def update_scheme(scheme_id):
    s = Scheme.query.get_or_404(scheme_id)
    data = request.json or {}
    for k in ['category','min_age','max_age','min_income','max_income','target_gender','states_applicable','start_date','end_date','official_url','active']:
        if k in data:
            setattr(s, k, data[k])
    db.session.commit()
    return jsonify({'status':'ok'})

@admin_bp.route('/schemes/<scheme_id>', methods=['DELETE'])
def delete_scheme(scheme_id):
    s = Scheme.query.get_or_404(scheme_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'status':'deleted'})

@admin_bp.route('/schemes/<scheme_id>/translations', methods=['POST'])
def add_translation(scheme_id):
    s = Scheme.query.get_or_404(scheme_id)
    data = request.json or {}
    lang = data.get('lang')
    if not lang:
        return jsonify({'error':'lang required'}), 400
    t = SchemeTranslation(
        scheme_id=s.id,
        lang=lang,
        title=data.get('title'),
        short_desc=data.get('short_desc'),
        full_desc=data.get('full_desc'),
        instructions=data.get('instructions'),
        last_updated=datetime.utcnow()
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id}), 201

@admin_bp.route('/schemes/<scheme_id>/translations/<lang>', methods=['PUT'])
def update_translation(scheme_id, lang):
    s = Scheme.query.get_or_404(scheme_id)
    t = SchemeTranslation.query.filter_by(scheme_id=s.id, lang=lang).first()
    if not t:
        return jsonify({'error':'not found'}), 404
    data = request.json or {}
    for f in ['title','short_desc','full_desc','instructions']:
        if f in data:
            setattr(t, f, data[f])
    t.last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify({'status':'ok'})

@admin_bp.route('/schemes/<scheme_id>/auto_translate', methods=['POST'])
def auto_translate(scheme_id):
    """Auto-translate stub: in real app call Google/DeepL. Here we copy English to requested lang with a marker."""
    s = Scheme.query.get_or_404(scheme_id)
    data = request.json or {}
    target_lang = data.get('lang')
    if not target_lang:
        return jsonify({'error':'lang required'}), 400
    # find english translation
    en = SchemeTranslation.query.filter_by(scheme_id=s.id, lang='en').first()
    if not en:
        return jsonify({'error':'no en source'}), 400
    t = SchemeTranslation(
        scheme_id=s.id,
        lang=target_lang,
        title=f"[AUTO] {en.title}",
        short_desc=f"[AUTO] {en.short_desc}",
        full_desc=f"[AUTO] {en.full_desc}",
        instructions=f"[AUTO] {en.instructions}"
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id, 'note':'auto-translated (stub)'}), 201
