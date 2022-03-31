from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_app.api_models import api_similarity, api_neighbor, one_neighb
from flask_app.get_secret import get_secret_word

MODEL = 'ruwikiruscorpora_upos_cbow_300_10_2021'
FORMAT = 'csv'
#secret_word = 'свинья'
secret_word = get_secret_word()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#db.create_all()


class Guesses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    similarity = db.Column(db.Float)
    closeness = db.Column(db.String)
#    secret = db.Column(db.String)

    def __repr__(self):
        return '<Guess %r>' % self.id


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        word_guess = request.form['content']
        new_similarity, new_closeness = api_similarity(MODEL, word_guess, secret_word)
        new_guess = Guesses(content=word_guess, similarity=new_similarity, closeness=new_closeness)
        try:
            db.session.add(new_guess)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your guess'

    else:
        guesses = Guesses.query.order_by(1 - Guesses.similarity).all()
        return render_template('index.html', guesses=guesses, secret_word=secret_word)

@app.route('/hints', methods=['GET','POST'])
def hints():
    # if request.method == 'POST':
    #     if request.form.get('hint') == 'Первая подсказка':
    #         pass
    #         #return render_template('hint_length.html', len_secret=len(secret_word))
    #     if request.form.get('hint') == 'Вторая подсказка':
    #         pass
    #         #return render_template('hint_length.html', len_secret=len(secret_word))
    # elif request.method == 'GET':
    return render_template('hints.html', len_secret=len(secret_word), neighb = one_neighb(api_neighbor(MODEL, secret_word, FORMAT)))

# @app.route('/hint_length', methods=['GET','POST'])
# def hint_length():
#     #len(secret_word)
#     return render_template('hint_length.html', len_secret=len(secret_word))


@app.route('/new_word', methods=['GET','POST'])
def new_word():
    try:
        db.session.query(Guesses).delete()
        db.session.commit()
        db.create_all()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

if __name__ == "__main__":
    app.run(debug=False)
