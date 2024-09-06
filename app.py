from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Initialize Flask-RESTX for Swagger support
api = Api(app, version='1.0', title='Flask MySQL API',
          description='A simple Flask API for interacting with MySQL database')

# Define the model for user input/output for Swagger
user_model = api.model('User', {
    'name': fields.String(required=True, description='Name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# Database connection function
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='flaskdb',
            user='flaskuser',
            password='flaskpassword'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# API Routes
@api.route('/users')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        """List all users"""
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(users)

    @api.expect(user_model)
    @api.doc('create_user')
    def post(self):
        """Create a new user"""
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "User created successfully!"}, 201

@api.route('/users/<int:id>')
class User(Resource):
    @api.doc('get_user')
    def get(self, id):
        """Get a user by ID"""
        connection = create_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            return jsonify(user)
        else:
            return {"message": "User not found!"}, 404

    @api.expect(user_model)
    @api.doc('update_user')
    def put(self, id):
        """Update a user"""
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "User updated successfully!"}

    @api.doc('delete_user')
    def delete(self, id):
        """Delete a user"""
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "User deleted successfully!"}

# Save the swagger.json file to the local file system
# @app.route('/swagger.json')
# def swagger_json():
#     return jsonify(api.__schema__)  # This generates the OpenAPI spec (swagger.json)


if __name__ == '__main__':
    app.run(debug=True)
