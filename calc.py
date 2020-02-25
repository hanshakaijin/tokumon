from flask import Flask, jsonify, request
import mlCard

app = Flask(__name__)
ml = mlCard.MlCard()

@app.route('/calc')
def c():
    tokumon = request.args.get('tokumon').split(',')
    algorithm = request.args.get('algorithm')
    score = ml.calc_cv_score(tokumon, int(algorithm))
    return jsonify(score)

if __name__ == "__main__":
    app.run(port=5000, debug=True)