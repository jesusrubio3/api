
from flask import Flask, render_template, abort, request
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os


app = Flask(__name__)

@app.route('/')
def inicio():
    key=os.environ["key"]
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD'
}
    headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': key ,
}

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        data=data.get("data")
        
        lista=[]
        valor=[]
        for i in data:
            a=i.get("name")
            lista.append(a)
            b=i.get("quote").get("USD").get("price")
            b=round(b, 2)
            valor.append(b)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    return render_template("inicio.html",e=zip(lista,valor))

@app.route('/cripto/<cripto>')
def criptomoneda(cripto):
    key=os.environ["key"]
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD'
}
    headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': key,
}

    session = Session()
    session.headers.update(headers)

    try:
        cripto=cripto.capitalize()
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        data=data.get("data")
        
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    return render_template("cripto.html",data=data,cripto=cripto)




@app.route('/conv',methods=["GET","POST"])
def suma():
    if request.method=="GET":
        key=os.environ["key"]
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
    'start':'1',
    'limit':'10',
    'convert':'USD'
    }
        headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': key,
    }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            data=data.get("data")
            seleccionado="Bitcoin"
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        return render_template("form.html",datas=data,seleccionado=seleccionado)
    

    else:
        key=os.environ["key"]
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
    'start':'1',
    'limit':'10',
    'convert':'USD'
    }
        headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': key,
    }

        session = Session()
        session.headers.update(headers)
        cantidad=request.form.get("numero1")
        moneda_id=request.form.get("monedas")

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            data=data.get("data")
            
            for i in data:
                
                if int(moneda_id)==int(i.get("id")):
                    nombre=i.get("name")
                    valor=i.get("quote").get("USD").get("price")
            conversion=float(cantidad)*float(valor)
            conversion=round(conversion,2)

        except:
            abort(404)
        return render_template("suma.html", cantidad=cantidad, moneda=moneda_id,nombre=nombre,conversion=conversion)
port=os.environ["PORT"]
app.run('0.0.0.0', int(PORT), debug=False)