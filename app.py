from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
import random
from sqlalchemy import func
from flask_migrate import Migrate

# Import the models and the extractor function
from models import Example, Entry, db
from extractor import extract_examples

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jfjdk12KDkfj3kD'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///examples.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

Migrate(app, db)

@app.route('/')
def index():
    """
    Renders the index.html template with a list of randomly selected examples.

    Returns:
        flask.Response: The rendered HTML template.
    """
    examples = Example.query.order_by(func.random()).limit(5).all()
    return render_template('index.html', examples=examples)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/learn')
def learn():
    example = Example.query.order_by(func.random()).first()
    return render_template('learn.html', example=example)

@app.route('/add_example', methods=['POST'])
def add_example():
    data = request.get_json()
    extracted_examples = extract_examples(data)
    for text, mark, end, audio_file in extracted_examples:
        example = Example(text=text, mark=mark, end=end, audio_file=audio_file)
        db.session.add(example)
    db.session.commit()
    return jsonify({'message': 'Examples added successfully'}), 201

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_string = request.form['query']
        response = requests.get(f'https://lod.lu/api/lb/search?query={search_string}&lang=lb')
        results = response.json()
        return render_template('search_results.html', results=results)
    return render_template('search.html')

@app.route('/display_examples', methods=['GET'])
def display_examples():
    entry_id = request.args.get('id')
    if entry_id:
        # Check if the entry already exists in the database
        entry = Entry.query.filter_by(entry_id=entry_id).first()
        if entry:
            # Entry exists in the database, load examples from the database
            example_objects = entry.examples
            loaded_from_db = True
        else:
            # Entry does not exist in the database, fetch examples from the external API
            response = requests.get(f'https://lod.lu/api/lb/entry/{entry_id}')
            data = response.json()
            extracted_examples = extract_examples(data)
            example_objects = [Example(text=text, mark=mark, end=end, audio_file=audio_file) for text, mark, end, audio_file in extracted_examples]
            loaded_from_db = False

            # Save the entry and examples to the database
            if example_objects:
                entry = Entry(entry_id=entry_id)
                db.session.add(entry)
                for example_obj in example_objects:
                    example_obj.entry = entry
                    db.session.add(example_obj)
                db.session.commit()

        return render_template('display_examples.html', entry_id=entry_id, 
                               examples=example_objects, loaded_from_db=loaded_from_db)
    return jsonify({'message': 'ID parameter is required'}), 400

@app.route('/entries')
def entries():
    """
    Renders the entries.html template with all the entries saved in the database.

    Returns:
        flask.Response: The rendered HTML template.
    """
    all_entries = Entry.query.all()
    return render_template('entries.html', entries=all_entries)

@app.route('/delete_entry/<string:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """
    Deletes an entry with the given entry_id and all linked examples.

    Args:
        entry_id (int): The ID of the entry to delete.

    Returns:
        flask.Response: The JSON response indicating the success or failure of the deletion.
    """
    entry = Entry.query.filter_by(entry_id=entry_id).first()
    if entry:
        # Delete all associated examples
        Example.query.filter_by(entry_id=entry.id).delete()

        # Delete the entry
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'Entry deleted successfully'}), 200
    else:
        return jsonify({'message': 'Entry not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

