from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('.index'))
    return render_template('login.html', error=error)

@app.route('/load_options', methods=['GET','POST'])
def load_options():
	error=None
	if request.method == 'POST':
		if request.form.get['load_data'] == "load_data":
			# Load input data
			pass
		elif request.form.get['load_weather'] == "load_weather":
			# load weather data
			pass
		elif request.form.get['train'] == "train":
			# train the model
			pass
		elif request.form.get['forecast'] == "forecast":
			return redirect(url_for('.forecast'))
		else:
			pass
	return render_template('load_options.html', error=error)
	
@app.route('/forecast')
def index(chartID = 'chart_ID', chart_type = 'spline', chart_width = 600, chart_height = 450):
	act, pred = compute_data('output_load_forecasting_result.txt')
	t_data = compute_data_single('rc15.txt')
	rain = compute_data_single('rain.txt')
	temp = compute_data_single('temp.txt')
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Predicted', "data": pred}, {"name": 'Actual', "data": act}, {"name": "Rain", "data" : rain}, 
		   {"name": "Training Data", "data": t_data}, {"name": "Temp", "data": temp}]
	title = {"text": 'Load Forecasting'}
	xAxis = {"title": {"text": 'Time'}}
	yAxis = {"title": {"text": 'Load'}}
	return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

def compute_data(f_name):
	input_vals = []
	output_vals = []

	with open(f_name, 'r') as f:
		d = f.readlines()
		for i in range(len(d)):
			input_vals.append(float(d[i].split(" ")[0]))
			output_vals.append(float(d[i].split(" ")[1]))

	return input_vals, output_vals

def compute_data_single(f_name):

	all_vals = []
	with open(f_name, 'r') as f:
		d = f.readlines()
		for i in range(len(d)):
			all_vals.append(float(d[i]))
			all_vals.append(float(d[i]))

	return all_vals
if __name__ == "__main__":
	app.run(debug = True, host='0.0.0.0', port=5000)#, passthrough_errors=True)
