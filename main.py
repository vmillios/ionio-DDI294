from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import sqlite3
from db_init import init_db, DB_NAME, CONFIG
from auth import require_auth

app = Flask(__name__)
swagger = Swagger(app)

@require_auth
@swag_from('swagger/get_customer_by_id.yml')
@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id: int):
        """
            Get customer data by customer ID
            ---
            security:
                - ApiKeyAuth: []
            parameters:
                - name: customer_id
                  in: path
                  type: integer
                  required: true
                  description: The ID of the customer
            responses:
                200:
                    description: Customer data or not found
                    examples:
                        application/json:
                            id: 1
                            name: Customer1
                            email: customer1@example.com
                            age: 21
        """
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('SELECT id, name, email, age FROM customers WHERE id = ?', (customer_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}
        else:
            return {"error": "Customer not found"}, 404


@app.route('/search_customer', methods=['POST'])
@require_auth
def search_customer():
    """
    Search for a customer by email
    ---
    parameters:
        - name: email
          in: formData
          type: string
          required: true
          description: Customer email to search for
    responses:
        200:
            description: Customer data or not found
            examples:
                application/json:
                    id: 1
                    name: Customer1
                    email: customer1@example.com
                    age: 21
    """
    email = request.form.get('email')
    if not email:
        return {"error": "Email parameter is required"}, 400
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, name, email, age FROM customers WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}
    else:
        return {"error": "Customer not found"}, 404

@app.route('/')
def hello():
        """
        A simple endpoint returning Hello
        ---
        responses:
            200:
                description: Returns Hello
                examples:
                    text: Hello
        """
        return 'Hello'

if __name__ == '__main__':
    init_db()
    app.run(
        debug=CONFIG.get('debug', True),
        host=CONFIG.get('host', '127.0.0.1'),
        port=CONFIG.get('port', 5000)
    )
