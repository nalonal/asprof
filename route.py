from app import *

@app.route('/')
def route_file():
	title = 'Indonesia Issue Crawler'
	return render_template(setup.PATH_TEMPLATE, title=title, page='beranda', view_file='index')

@app.route('/login')
def login_page():
	title = 'Halaman Login Pengguna'
	return render_template(setup.PATH_TEMPLATE_LOGIN, title=title)

@app.route('/literature_review')
def literature_review():
	output = {}
	conn = dbcon()
	title = ' Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("select * from research_slr")
	data = cur.fetchall()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, title=title, page='literature_review', view_file='index', output = output)	


#literature review id
@app.route('/literature_review/<id>',methods = ['POST', 'GET'])
def literature_review_id(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_information', output = output)	

@app.route('/literature_review/update',methods = ['POST'])
@cross_origin()
def literature_review_update():
	conn = dbcon()
	cur = conn.cursor()
	data = request.get_json()
	id = data['id']
	research_title = data['research_title']
	research_author = data['research_author']
	cur.execute('UPDATE research_slr SET research_title=%s, research_author=%s WHERE id=%s',[research_title,research_author,id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/update_map',methods = ['POST'])
@cross_origin()
def literature_review_update_map():
	conn = dbcon()
	cur = conn.cursor()
	data = request.get_json()
	id = data['id']
	research_introduction = data['research_introduction']
	research_literature = data['research_literature']
	research_methodology = data['research_methodology']
	research_keyword = data['research_keyword']
	cur.execute('UPDATE research_slr SET research_introduction=%s,  research_literature=%s, research_methodology=%s, research_keyword=%s WHERE id=%s',[research_introduction,research_literature,research_methodology,research_keyword,id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/delete',methods = ['POST'])
@cross_origin()
def literature_review_delete():
	conn = dbcon()
	cur = conn.cursor()
	data = request.get_json()
	id = data['id']
	cur.execute('DELETE from research_slr WHERE id=%s',[id])
	conn.commit()

	cur.execute('DELETE from paragraph_tb WHERE research_id=%s',[id])
	conn.commit()

	cur.execute('DELETE from references_tb WHERE research_id=%s',[id])
	conn.commit()

	return Response(json.dumps(data),status=200, mimetype='application/json')

#literature review id
@app.route('/literature_review/<id>/ri',methods = ['POST', 'GET'])
def literature_review_ri(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_identification', output = output)	

@app.route('/literature_review/<id>/rk')
def literature_review_rk(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_keyword', output = output)	



@app.route('/literature_review/<id>/as')
def literature_review_as(id):
	output = {}
	status = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()

	cur.execute("select status from paragraph_tb where research_id="+id+" AND category='introduction'")
	data_introduction = cur.fetchone()
	if(data_introduction):
		status_introduction = True
	else:
		status_introduction = False

	cur.execute("select status from paragraph_tb where research_id="+id+" AND category='literature'")
	data_literature = cur.fetchone()
	if(data_literature):
		status_literature= True
	else:
		status_literature = False

	cur.execute("select status from paragraph_tb where research_id="+id+" AND category='methodology'")
	data_methodology = cur.fetchone()
	if(data_methodology):
		status_methodology= True
	else:
		status_methodology= False


	cur.execute("select * from references_tb where research_id="+id)
	data_total_references = cur.fetchall()
	total_references = len(data_total_references)

	cur.execute("select * from references_tb where research_id="+id+" AND doi IS NOT NULL")
	data_total_process_references = cur.fetchall()
	total_process_references = len(data_total_process_references)

	status['introduction'] = status_introduction
	status['literature'] = status_literature
	status['methodology'] = status_methodology
	status['total_references'] = total_references
	status['total_process_references'] = total_process_references

	output['data'] = data
	output['status'] = status
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_status', output = output)	
	
@app.route('/literature_review/<id>/lr')
def literature_review_lr(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_literature', output = output)	
	

@app.route('/literature_review/<id>/io')
def literature_review_io(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_output', output = output)	

@app.route('/literature_review/<id>/ie')
def literature_review_ie(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_export', output = output)	

@app.route('/literature_review/add', methods=['POST'])
@cross_origin()
def literature_review_add():
	conn = dbcon()
	data = request.get_json()
	research_title = data['research_title']
	research_author = data['research_author']
	status = "created"
	date_now = datetime.now().strftime("%Y-%m-%d")
	research_map = '{ "class": "go.TreeModel","nodeDataArray": [{"key":0, "text":"Implementation Big Data in Cyber Security : Systematic Literature Review", "loc":"-202.63350000000025 94.32549999999998"},{"key":1, "parent":0, "text":"Introduction", "brush":"skyblue", "dir":"right", "loc":"241.48515234374975 78.82549999999998"},{"key":3, "parent":0, "text":"Literature Study", "brush":"palevioletred", "dir":"right", "loc":"241.48515234374975 104.82549999999998"},{"key":4, "parent":0, "text":"Research Methods", "brush":"coral", "dir":"right", "loc":"241.48515234374975 130.82549999999998"}]}'
	cur = conn.cursor()
	cur.execute("INSERT INTO research_slr(research_title, research_author,status,created_date, research_map) \
                    SELECT %s,%s,%s,%s,%s WHERE NOT EXISTS(SELECT 1 FROM research_slr WHERE research_title = %s AND research_author = %s)",(research_title,research_author,status,date_now,research_map,research_title,research_author))
	conn.commit()	
	return Response(json.dumps(data),status=200, mimetype='application/json')

##SETTINGS PAGE
@app.route('/setting')
def setting():
	output = {}
	conn = dbcon()
	title = 'Setting Page'
	# conn.row_factory = sql.Row
	cur = conn.cursor()
	data = {}
	#select facebook token
	cur.execute("select * from config where title='FACEBOOK_SESSION'")
	_ = cur.fetchone()
	data['FACEBOOK_SESSION'] = _[3]
	#select opengpt session 1
	cur.execute("select * from config where title='OPENGPT_SESSION_1'")
	_ = cur.fetchone()
	data['OPENGPT_SESSION_1'] = _[3]
	#select opengpt session 2
	cur.execute("select * from config where title='OPENGPT_SESSION_2'")
	_ = cur.fetchone()
	data['OPENGPT_SESSION_2'] = _[3]
	#select opengpt session 3
	cur.execute("select * from config where title='OPENGPT_SESSION_3'")
	_ = cur.fetchone()
	data['OPENGPT_SESSION_3'] = _[3]
	#select opengpt session 4
	cur.execute("select * from config where title='OPENGPT_SESSION_4'")
	_ = cur.fetchone()
	data['OPENGPT_SESSION_4'] = _[3]
	print(data)
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, title=title, page='setting', view_file='page', output = output)	
	
@app.route('/setting/update', methods=['POST'])
@cross_origin()
def setting_update():
	conn = dbcon()
	cur = conn.cursor()
	data = request.get_json()
	update_data = {
        'FACEBOOK_SESSION': data['FACEBOOK_SESSION'],
		'OPENGPT_SESSION_1': data['OPENGPT_SESSION_1'],
		'OPENGPT_SESSION_2': data['OPENGPT_SESSION_2'],
		'OPENGPT_SESSION_3': data['OPENGPT_SESSION_3'],
		'OPENGPT_SESSION_4': data['OPENGPT_SESSION_4'],
    }
	if(update_data['FACEBOOK_SESSION'] != ""):
		cur.execute('UPDATE config SET value=%s WHERE title="FACEBOOK_SESSION"',[update_data['FACEBOOK_SESSION']])
		conn.commit()
	if(update_data['OPENGPT_SESSION_1'] != ""):
		cur.execute('UPDATE config SET value=%s WHERE title="OPENGPT_SESSION_1"',[update_data['OPENGPT_SESSION_1']])
		conn.commit()
	if(update_data['OPENGPT_SESSION_2'] != ""):
		cur.execute('UPDATE config SET value=%s WHERE title="OPENGPT_SESSION_2"',[update_data['OPENGPT_SESSION_2']])
		conn.commit()
	if(update_data['OPENGPT_SESSION_3'] != ""):
		cur.execute('UPDATE config SET value=%s WHERE title="OPENGPT_SESSION_3"',[update_data['OPENGPT_SESSION_3']])
		conn.commit()
	if(update_data['OPENGPT_SESSION_4'] != ""):
		cur.execute('UPDATE config SET value=%s WHERE title="OPENGPT_SESSION_4"',[update_data['OPENGPT_SESSION_4']])
		conn.commit()
	# print(update_data)
	return Response(json.dumps(update_data),status=200, mimetype='application/json')


@app.route('/api/automate_openai', methods=['POST'])
@cross_origin()
def automate_openai():
	data = request.get_json()
	id = data['id']
	# getOpenAPI = GetOpenAPI(id)
	# getOpenAPI.start()
	getLibrary = GetLibrary(id)
	getLibrary.start()
	return {'status': 'ok'}, 200
	
app.run(debug = True) if __name__ == '__main__' else "Error"