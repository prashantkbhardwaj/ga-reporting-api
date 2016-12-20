import analytics_core as ac
from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hi!"

@app.route("/campaign", methods=['GET', 'POST'])
def campaign_sessions():
	campaign = request.args.get('name')
	startDate = request.args.get('startdate')
	endDate = request.args.get('enddate')
	
	analytics = ac.initialize_analyticsreporting()
	
	try:
		response = ac.get_report(analytics, campaign=campaign, startDate=str(startDate), endDate=str(endDate))
	except Exception as e:
		return jsonify({'error': str(e) })

	session_value = ac.print_response(response)
	return jsonify({'Source': campaign, 'startDate': startDate, 'endDate': endDate, 'sessions': session_value})

@app.route("/source", methods=['GET', 'POST'])
def source_sessions():
	source = request.args.get('name')
	startDate = request.args.get('startdate')
	endDate = request.args.get('enddate')


	analytics = ac.initialize_analyticsreporting()

	try:
		response = ac.get_report(analytics, source=source, startDate=str(startDate), endDate=str(endDate))
	except Exception as e:
		return jsonify({'error': str(e) })

	session_value = ac.print_response(response)
	return jsonify({'Source': source, 'startDate': startDate, 'endDate': endDate, 'sessions': session_value})


if __name__ == '__main__':
  app.run(debug=True)