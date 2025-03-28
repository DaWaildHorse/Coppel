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

def mayores5(df):

    # Calcular el promedio del tiempo de espera por estado
    promedios_por_estado = df.groupby('estado')['tiempo_espera'].mean()
    # Obtener los 5 estados con mayor tiempo promedio
    top_5_estados = promedios_por_estado.nlargest(5)
    # Convertir los valores a formato hh:mm:ss
    top_5_estados_hms = top_5_estados.apply(horas_a_hms)
    return top_5_estados_hms.to_dict()
    

def mayorespera(df):
    # Calcular el promedio del tiempo de atención por estado
    promedios_por_estado_atencion = df.groupby('estado')['tiempo_atencion'].mean()

    # Obtener los 5 estados con mayor tiempo promedio de tiempo_atencion
    top_5_estados_mayores_atencion = promedios_por_estado_atencion.nlargest(5)
    # Convertir los valores a formato hh:mm:ss
    top_5_estados_mayores_hms_atencion = top_5_estados_mayores_atencion.apply(horas_a_hms)
    return top_5_estados_mayores_hms_atencion.to_dict()


def distribucion(df):
    # Count total occurrences of each status
    status_counts = df['status'].value_counts(normalize=True) * 100

    # Format the output
    result = '  '.join([f"{status} : {int(percent)}%" for status, percent in status_counts.items()])

    return result



@app.route("/dash1", methods=['GET'])
def dash1():
    df = pd.read_csv('EDA/sample_data.csv')
    menores5_result = menores5(df)
    return jsonify(menores5_result)  # Return as JSON response


@app.route("/dash2", methods=['GET'])
def dash2():
    df = pd.read_csv('EDA/sample_data.csv')
    menores5_result = mayores5(df)
    return jsonify(menores5_result)  # Return as JSON response

@app.route("/dash3", methods=['GET'])
def dash3():
    df = pd.read_csv('EDA/sample_data.csv')
    mayores5_result = mayorespera(df)
    return jsonify(mayores5_result)  # Return as JSON response

@app.route("/dash4", methods=['GET'])
def dash4():
    df = pd.read_csv('EDA/sample_data.csv')
    distr = distribucion(df)
    return jsonify(distr)  # Return as JSON response




if __name__ == "__main__":
    app.run(debug=True, port=8080)


