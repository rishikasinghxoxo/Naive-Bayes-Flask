from flask import Flask, render_template_string, request
import pandas as pd
import os
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

app = Flask(__name__)

os.makedirs("static", exist_ok=True)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Naive Bayes Trainer</title>
</head>

<body>

<h1>Naive Bayes Machine Learning Trainer</h1>

<form method="POST" enctype="multipart/form-data">

Upload CSV Dataset:
<input type="file" name="file" required>

<br><br>

Target Column:
<input type="text" name="target" placeholder="Enter target column name" required>

<br><br>

<button type="submit">Train Model</button>

</form>

{% if preview %}

<h2>Dataset Preview</h2>
{{preview|safe}}

{% endif %}

{% if accuracy %}

<h2>Model Accuracy: {{accuracy}}</h2>

<h3>Confusion Matrix</h3>
<img src="{{cm_image}}" width="400">

{% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():

    accuracy = None
    cm_image = None
    preview = None

    if request.method == "POST":

        file = request.files["file"]
        target = request.form["target"]

        df = pd.read_csv(file)

        preview = df.head().to_html()

        # Encoding categorical columns
        df = pd.get_dummies(df, drop_first=True)

        # Ensure target exists
        if target not in df.columns:
            return render_template_string(
                HTML_PAGE,
                preview=preview,
                accuracy=None,
                cm_image=None
            )

        X = df.drop(columns=[target])
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42
        )

        model = GaussianNB()

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = round(accuracy_score(y_test, y_pred), 4)

        cm = confusion_matrix(y_test, y_pred)

        fig, ax = plt.subplots()
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(ax=ax)

        cm_image = "static/confusion_matrix.png"
        plt.savefig(cm_image)
        plt.close()

    return render_template_string(
        HTML_PAGE,
        preview=preview,
        accuracy=accuracy,
        cm_image=cm_image
    )


if __name__ == "__main__":
    app.run(debug=True)