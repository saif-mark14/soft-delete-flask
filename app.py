from flask import Flask,jsonify,request
from models import db,User

app = Flask(__name__)

# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create DB tables
with app.app_context():
    db.create_all()


# Create User
@app.route("/add", methods=["POST"])
def add_user():
    name = request.json['name']
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message":"User added"}),201

# GET User(only non-deleted)
@app.route("/users",methods=["GET"])
def get_users():
    users = User.query.filter_by(is_deleted=False).all()
    result = [{"id": u.id, "name": u.name} for u in users]
    return jsonify(result)

# Soft Delete
@app.route("/delete/<int:id>",methods=["DELETE"])
def soft_delete(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify({"error":"User not found"}),404

    user.is_deleted = True
    db.session.commit()

    return jsonify({"message":"User soft deleted"})


# GET Soft Deleted Users
@app.route("/deleted-users",methods=["GET"])
def get_deleted_users():
    deleted_users = User.query.filter_by(is_deleted=True).all()
    result = [{"id": u.id, "name": u.name} for u in deleted_users]
    return jsonify(result)

# Check user status
@app.route("/user/<int:id>",methods=["GET"])
def check_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"error":"User not found"}),404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "is_deleted": user.is_deleted
    })

# Restore User
@app.route("/restore/<int:id>",methods=["PUT"])
def restore_user(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify({"error":"User not found"}),404

    user.is_deleted = False
    db.session.commit()

    return jsonify({"message":"User restored"})

if __name__ == "__main__":
    app.run(debug=True)
