from flask import Flask, jsonify, request 
import yfinance as yf
import pandas as pd
import math
  
# creating a Flask app 
app = Flask(__name__) 
  
# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 

@app.route('/', methods = ['GET', 'POST']) 
def display_quote():
	# get a stock ticker symbol from the query string
	# default to AAPL

	df = pd.read_csv('fidelitytickers.csv')
	tickers_list = df["Tickers"].to_list()

	symbol = request.args.get('symbol', default=tickers_list[:500])

	quote = yf.download(symbol, period="1d", interval="1d", progress=False)["Close"].head(1)

	quote.reset_index(drop=True, inplace=True)

	quote = quote.to_dict()
	
	for key in quote:
		quote[key] = quote[key][0]
		if math.isnan(quote[key]):
			quote[key] = "NaN"

	return jsonify(quote)
  
  
# A simple function to calculate the square of a number 
# the number to be squared is sent in the URL when we use GET 
# on the terminal type: curl http://127.0.0.1:5000 / home / 10 
# this returns 100 (square of 10) 
@app.route('/home/<int:num>', methods = ['GET']) 
def disp(num): 
  
    return jsonify({'data': num**2, "data2": num**2}) 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True, use_reloader = True) 