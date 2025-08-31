from flask import Blueprint, request, jsonify
from models import db, Scheme, SchemeTranslation
from sqlalchemy import or_
from babel.dates import format_date

api_bp = Blueprint('api', __name__)


def translate_scheme(scheme, lang='en'):
    t = next((tr for tr in scheme.translations if tr.lang == lang), None)
    if not t:
        t = next((tr for tr in scheme.translations if tr.lang == 'en'), None)
    translations = [{'lang': tr.lang, 'title': tr.title, 'short_desc': tr.short_desc} for tr in scheme.translations]
    return {
        'id': scheme.id,
        'code': scheme.code,
        'category': scheme.category,
        'title': t.title if t else None,
        'short_desc': t.short_desc if t else None,
        'full_desc': t.full_desc if t else None,
        'instructions': t.instructions if t else None,
        'states_applicable': scheme.states_applicable,
        'start_date': format_date(scheme.start_date, locale=lang) if scheme.start_date else None,
        'end_date': format_date(scheme.end_date, locale=lang) if scheme.end_date else None,
        'official_url': scheme.official_url,
        'translations': translations
    }

def list_schemes():
    q = request.args.get('q','').strip()
    lang = request.args.get('lang','en')
    state = request.args.get('state')
    category = request.args.get('category')
    page = int(request.args.get('page',1))
    per_page = int(request.args.get('per_page',10))

    query = Scheme.query.filter(Scheme.active == True)
    if state:
        query = query.filter(or_(Scheme.states_applicable==None, Scheme.states_applicable.contains([state])))
    if category:
        query = query.filter(Scheme.category.ilike(f'%{category}%'))
    if q:
        translations = SchemeTranslation.query.filter(
            SchemeTranslation.lang.in_([lang, 'en']),
            or_(
                SchemeTranslation.title.ilike(f'%{q}%'),
                SchemeTranslation.short_desc.ilike(f'%{q}%')
            )
        ).with_entities(SchemeTranslation.scheme_id).all()
        ids = [t.scheme_id for t in translations]
        if ids:
            query = query.filter(Scheme.id.in_(ids))
        else:
            query = query.filter(Scheme.id == '')  # no results

    pag = query.order_by(Scheme.created_at.desc()).paginate(page, per_page, False)
    items = [translate_scheme(s, lang) for s in pag.items]
    return jsonify({
        'total': pag.total,
        'page': page,
        'per_page': per_page,
        'items': items
    })

@api_bp.route('/schemes/<scheme_id>', methods=['GET'])
def get_scheme(scheme_id):
    lang = request.args.get('lang', 'en')
    scheme = Scheme.query.get_or_404(scheme_id)
    return jsonify(translate_scheme(scheme, lang))

@api_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.json or {}
    age = data.get('age')
    gender = data.get('gender')
    income = data.get('income')
    state = data.get('state')
    lang = data.get('lang','en')

    query = Scheme.query.filter(Scheme.active == True)
    if age:
        query = query.filter(or_(Scheme.min_age==None, Scheme.min_age <= age))
        query = query.filter(or_(Scheme.max_age==None, Scheme.max_age >= age))
    if income:
        query = query.filter(or_(Scheme.min_income==None, Scheme.min_income <= income))
        query = query.filter(or_(Scheme.max_income==None, Scheme.max_income >= income))
    if state:
        query = query.filter(or_(Scheme.states_applicable==None, Scheme.states_applicable.contains([state])))

    results = query.limit(50).all()
    scored = []
    for s in results:
        score = 0
        if s.target_gender and gender and s.target_gender.lower() == gender.lower():
            score += 5
        if s.states_applicable and state and state in s.states_applicable:
            score += 3
        scored.append((score, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    items = [translate_scheme(s, lang) for score,s in scored[:20]]
    return jsonify({'items': items})
