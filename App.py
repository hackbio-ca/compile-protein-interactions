#iConnecting backend and frontend thru Flask API
from flask import Flask, jsonify
from connections import driver  # your Neo4j connection script

app = Flask(__name__)

@app.route("/api/test")
def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Backend Connected!' AS msg")
        return jsonify(msg=result.single()["msg"])

if __name__ == "__main__":
    app.run(debug=True)
