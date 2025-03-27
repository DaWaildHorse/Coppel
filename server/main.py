from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Función para convertir horas decimales a hh:mm:ss
def horas_a_hms(horas):
    segundos_totales = round(horas * 3600)
    h, m, s = segundos_totales // 3600, (segundos_totales % 3600) // 60, segundos_totales % 60
    return f"{h:02}:{m:02}:{s:02}"

def menores5(df):
    promedios_por_estado = df.groupby('estado')['tiempo_espera'].mean()
    top_5_estados_menores = promedios_por_estado.nsmallest(5)
    top_5_estados_menores_hms = top_5_estados_menores.apply(horas_a_hms)
    return top_5_estados_menores_hms.to_dict()  # Convert to dictionary for JSON response

@app.route("/main", methods=['GET'])
def users():
    df = pd.read_csv('EDA/sample_data.csv')
    menores5_result = menores5(df)
    return jsonify(menores5_result)  # Return as JSON response

if __name__ == "__main__":
    app.run(debug=True, port=8080)
