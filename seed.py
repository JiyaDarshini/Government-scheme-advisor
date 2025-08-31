# Simple seed script to create example scheme entries
from app import create_app
from models import db, Scheme, SchemeTranslation
from datetime import date

app = create_app()
with app.app_context():
    db.create_all()
    s = Scheme(
        code="SCHOLAR_2025",
        category="Education",
        min_age=18, max_age=25,
        states_applicable=None,
        start_date=date(2024,1,1),
        end_date=None,
        official_url="https://gov.example/scholarship",
        active=True
    )
    db.session.add(s)
    db.session.commit()
    t_en = SchemeTranslation(scheme_id=s.id, lang='en',
                              title='Merit Scholarship for Students',
                              short_desc='Financial aid for meritorious students.',
                              full_desc='Full details go here.')
    t_hi = SchemeTranslation(scheme_id=s.id, lang='hi',
                              title='छात्रों के लिए मेरिट छात्रवृत्ति',
                              short_desc='प्रतिभावान छात्रों के लिए आर्थिक सहायता।',
                              full_desc='विस्तृत विवरण यहां।')
    db.session.add_all([t_en, t_hi])
    db.session.commit()
    print('Seeded example scheme.')
