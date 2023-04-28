import response as response
from flask import Flask, jsonify, request
from re import search
import requests

app = Flask(__name__)

# sample data
# introduce Luigi, kubernetes, postman

books = [
    {"id": 1, "title": "Python Programming", "author": "John Smith"},
    {"id": 2, "title": "Java Programming", "author": "Jane Doe"}
]

properties = [
    {"id": 1, "title": "Property for sale in xxxxxxx", "realtor_name": "John Smith", "Description": "Something to "
                                                                                                    "describe",
     "poster_frame": "path to poster frame", "Gallery": "Array of photos"},
]

# GET /houses?country=nigeria&state=lagos&local_govt=<local_govt>&town=<town>&for_sale=true
url, headers = 'https://localhost.com/houses', {'Content-Type': 'application/json'}
query = """{
  houses(state: "nigeria", localGovt: "<local_govt>", town: "<town>", forSale: true) {
    address
    price
    description
    agent {
      name
      phone
    }
  }
}
"""
payload = {'query': query}

# GET request
response, json_response = requests.get(url, headers=headers, params=payload), response.json()


# Publish
@app.route('/api/property', methods=['POST'])
def publish_properties():
    return jsonify(properties)


# API endpoint to get all properties
# Introduce method Overloading
@app.route('/api/property', methods=['GET'])
def get_properties():
    return jsonify(properties)


# API endpoint to get a property ad by id
@app.route('/api/property/<int:id>', methods=['GET'])
def get_property(id):
    book = next((book for book in books if book['id'] == id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"message": "Book not found"}), 404


# API endpoint to add a property ad under a License of a registered realtor.
@app.route('/api/property/', methods=['POST'])
def add_property():
    properties = request.json
    properties["id"] = len(books) + 1
    books.append(properties)
    return jsonify(properties), 201


# API endpoint to add a book
@app.route('/api/books', methods=['POST'])
def add_book():
    book = request.json
    book["id"] = len(books) + 1
    books.append(book)
    return jsonify(book), 201


# API endpoint to update a book
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_property_ad(id):
    book = next((book for book in books if book['id'] == id), None)
    if book:
        book.update(request.json)
        return jsonify(book)
    else:
        return jsonify({"message": "Book not found"}), 404


# API endpoint to delete a book
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = next((book for book in books if book['id'] == id), None)
    if book:
        books.remove(book)
        return jsonify({"message": "Book deleted"})
    else:
        return jsonify({"message": "Book not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
