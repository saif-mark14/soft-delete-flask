import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User

def test_soft_delete():
    client = app.test_client()

    with app.app_context():
        user = User(name="Saif")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    response = client.get(f"/delete/{user_id}")
    assert response.status_code == 200

    with app.app_context():
        deleted_user = User.query.get(user_id)
        assert deleted_user.is_deleted is True
