from flask import Flask, request, render_template_string, jsonify
import pickle
from scoring_module import calculate_score
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)


loaded_model = pickle.load(open("model.pkl", "rb"))

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        input_text = request.form['text']

        prediction, probability = calculate_score(input_text, loaded_model, 0.55)

        response = {
            "prediction": prediction,
            "propensity": probability
        }

        return jsonify(response)
    else:
        return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Spam Classifier</title>
                <style>
                    body {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        flex-direction: column; /* Added */
                    }
                    h1 {
                        text-align: center;
                        margin-top: 20px; /* Adjusted */
                    }
                    form {
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <h1>Spam Classifier</h1>
                <form action="/" method="post">
                    <label for="text">Enter Text:</label><br>
                    <input type="text" id="text" name="text"><br><br>
                    <input type="submit" value="Submit">
                </form>
            </body>
            </html>
        """

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
