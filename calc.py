from flask import Flask, jsonify, request
import mlCard

app = Flask(__name__)
ml = mlCard.MlCard()

@app.route('/calc')
def c():
    tokumon = request.args.get('tokumon').split(',')
    algorithm = request.args.get('algorithm')
    dummy = request.args.get('dummy').split(',')
    fillna = request.args.get('fillna').split(',')

    #ignore dummy at 2 types category feature
    if 'cabin_isodd' in dummy:
        dummy.remove('cabin_isodd')
    
    features = [(t+"_fill_median" if (t in fillna) else t) for t in tokumon]
    features = [(t+"_dummy" if (t.replace("_fill_median", '') in dummy) else t) for t in features]
    print(features)
    score = ml.calc_cv_score(features, int(algorithm))
    return jsonify({k:("%2.1f" % (v*100)) for (k,v) in score.items()})

if __name__ == "__main__":
    app.run(port=5000, debug=True)