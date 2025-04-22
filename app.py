from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Lista de links baseados no CPF (igual ao seu HTML)
def gerar_links(cpf):
    links = [
        f"https://app.koofr.net/content/links/f90f54be-d570-4046-8311-de35808a3cb7/files/get/{cpf}.pdf?path=%2F{cpf}.pdf"
    ]
    links += [
        f"https://app.koofr.net/content/links/f90f54be-d570-4046-8311-de35808a3cb7/files/get/{cpf} ({i+1}).pdf?path=%2F{cpf}%20({i+1}).pdf"
        for i in range(19)
    ]
    return links

# Função para verificar se o link existe (usando GET com User-Agent)
def verificar_link(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except:
        return False

@app.route('/buscar_exame', methods=['GET'])
def buscar_exame():
    cpf = request.args.get('cpf', '').replace('.', '').replace('-', '')

    if len(cpf) != 11 or not cpf.isdigit():
        return jsonify({"resultado": "CPF inválido. Informe 11 dígitos."})

    links = gerar_links(cpf)
    resultados = []

    for idx, link in enumerate(links, 1):
        if verificar_link(link):
            resultados.append(f"Exame {idx}: {link}")

    if resultados:
        return jsonify({"resultado": "\n".join(resultados)})
    else:
        return jsonify({"resultado": "Nenhum exame encontrado para este CPF."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
