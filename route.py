from app import *

# @app.route('/')
# def route_file():
# 	title = 'Indonesia Issue Crawler'
# 	return render_template(setup.PATH_TEMPLATE, title=title, page='beranda', view_file='index')

@app.route('/login')
def login_page():
	title = 'Halaman Login Pengguna'
	return render_template(setup.PATH_TEMPLATE_LOGIN, title=title)

@app.route('/')
def literature_review():
	output = {}
	conn = dbcon()
	title = ' Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor(buffered=True)
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
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_information', output = output)	

@app.route('/literature_review/update',methods = ['POST'])
@cross_origin()
def literature_review_update():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['id']
	research_title = data['research_title']
	research_author = data['research_author']
	research_question = data['research_question']
	research_identification = data['research_identification']
	research_question_list_template = data['research_question_list_template']
	cur.execute('UPDATE research_slr SET research_title=%s, research_author=%s, research_question=%s, research_identification=%s, research_question_list_template=%s WHERE id=%s',[research_title,research_author,research_question,research_identification,research_question_list_template,id])
	
	
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/update/output',methods = ['POST'])
@cross_origin()
def literature_review_update_output():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['id']
	output = data['output']
	cur.execute('UPDATE research_slr SET output =%s WHERE id=%s',[output,id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')


@app.route('/literature_review/rk/update',methods = ['POST'])
@cross_origin()
def literature_review_rk_update():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['id']
	research_keyword = data['research_keyword']
	print(research_keyword)
	cur.execute('UPDATE research_slr SET research_keyword=%s WHERE id=%s',[research_keyword,id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/update_map',methods = ['POST'])
@cross_origin()
def literature_review_update_map():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['id']
	input_research_map = data['research_map']
	research_map = json.loads(input_research_map)
	data_results = research_map['nodeDataArray'] 
	introduction = []
	literature = []
	methodology = []

	for _ in data_results:
		try:
			parent = _['parent'] 
		except:
			parent = 0
			pass
		if(parent == 1):
			introduction.append(_['text'])
		if(parent == 3):
			literature.append(_['text'])
		if(parent == 4):
			methodology.append(_['text'])
	research_introduction = "\n".join(introduction)
	research_literature = "\n".join(literature)
	research_methodology = "\n".join(methodology)

	cur.execute('UPDATE research_slr SET research_introduction=%s,  research_literature=%s, research_methodology=%s, research_map=%s WHERE id=%s',[research_introduction,research_literature,research_methodology,input_research_map,id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/delete',methods = ['POST'])
@cross_origin()
def literature_review_delete():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['id']
	cur.execute('DELETE from research_slr WHERE id=%s',[id])
	conn.commit()

	cur.execute('DELETE from paragraph_tb WHERE research_id=%s',[id])
	conn.commit()

	cur.execute('DELETE from references_tb WHERE research_id=%s',[id])
	conn.commit()

	cur.execute('DELETE from slr_tb WHERE research_id=%s',[id])
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
	cur = conn.cursor(buffered=True)
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
	cur = conn.cursor(buffered=True)
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
	cur = conn.cursor(buffered=True)
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

	cur.execute("select * from slr_tb where research_id="+id+" AND source='ieee'")
	data_total_references = cur.fetchall()
	total_slr_iee = len(data_total_references)

	cur.execute("select * from slr_tb where research_id="+id+" AND source='ieee' AND status IS NOT NULL")
	data_total_process_references = cur.fetchall()
	total_process_slr_iee = len(data_total_process_references)

	cur.execute("select * from slr_tb where research_id="+id+" AND source='Sciencedirect'")
	data_total_references = cur.fetchall()
	total_slr_sd = len(data_total_references)

	cur.execute("select * from slr_tb where research_id="+id+" AND source='Sciencedirect' AND status IS NOT NULL")
	data_total_process_references = cur.fetchall()
	total_process_slr_sd = len(data_total_process_references)

	cur.execute("select * from slr_tb where research_id="+id+" AND source='ACM Digital Library'")
	data_total_references = cur.fetchall()
	total_slr_acm = len(data_total_references)

	cur.execute("select * from slr_tb where research_id="+id+" AND source='ACM Digital Library' AND status IS NOT NULL")
	data_total_process_references = cur.fetchall()
	total_process_slr_acm = len(data_total_process_references)


	cur.execute("select * from slr_tb where research_id="+id+" AND bibtex IS NOT NULL")
	data_total_references = cur.fetchall()
	total_process_bibtex = len(data_total_references)

	cur.execute("select * from slr_tb where research_id="+id)
	data_total_process_references = cur.fetchall()
	total_bibtex = len(data_total_process_references)

	
	status['introduction'] = status_introduction
	status['literature'] = status_literature
	status['methodology'] = status_methodology
	status['total_references'] = total_references
	status['total_process_references'] = total_process_references

	status['total_slr_iee'] = total_slr_iee
	status['total_process_slr_iee'] = total_process_slr_iee

	status['total_slr_sd'] = total_slr_sd
	status['total_process_slr_sd'] = total_process_slr_sd

	status['total_slr_acm'] = total_slr_acm
	status['total_process_slr_acm'] = total_process_slr_acm

	status['total_bibtex'] = total_bibtex
	status['total_process_bibtex'] = total_process_bibtex

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
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()

	output['data'] = data

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant IS NULL")
	output['papers'] = cur.fetchall()

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant IS NULL")
	total_papers = cur.fetchall()
	output['total_papers'] = len(total_papers)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='duplicated'")
	this_duplicated = cur.fetchall()
	output['duplicated'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	this_duplicated = cur.fetchall()
	output['relevant'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='unrelated'")
	this_duplicated = cur.fetchall()
	output['unrelevant'] = len(this_duplicated)

	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_literature', output = output)	


@app.route('/literature_review/<id>/rq')
def literature_review_rq(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_literature_researchquestion', output = output)	



@app.route('/literature_review/<id>/lr/related')
def literature_review_lr_related(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	output['papers'] = cur.fetchall()

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant IS NULL")
	total_papers = cur.fetchall()
	output['total_papers'] = len(total_papers)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='duplicated'")
	this_duplicated = cur.fetchall()
	output['duplicated'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	this_duplicated = cur.fetchall()
	output['relevant'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='unrelated'")
	this_duplicated = cur.fetchall()
	output['unrelevant'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='eliminated'")
	this_eliminated = cur.fetchall()
	output['eliminated'] = len(this_eliminated)

	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_literature_related', output = output)	

@app.route('/literature_review/<id>/lr/unrelated')
def literature_review_lr_unrelated(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='unrelated'")
	output['papers'] = cur.fetchall()

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant IS NULL")
	total_papers = cur.fetchall()
	output['total_papers'] = len(total_papers)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='duplicated'")
	this_duplicated = cur.fetchall()
	output['duplicated'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	this_duplicated = cur.fetchall()
	output['relevant'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='unrelated'")
	this_duplicated = cur.fetchall()
	output['unrelevant'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='eliminated'")
	this_eliminated = cur.fetchall()
	output['eliminated'] = len(this_eliminated)

	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_literature_unrelated', output = output)	


@app.route('/literature_review/<id>/lr/eliminated')
def literature_review_lr_eliminated(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='eliminated'")
	output['papers'] = cur.fetchall()

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant IS NULL")
	total_papers = cur.fetchall()
	output['total_papers'] = len(total_papers)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='duplicated'")
	this_duplicated = cur.fetchall()
	output['duplicated'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	this_duplicated = cur.fetchall()
	output['relevant'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='unrelated'")
	this_duplicated = cur.fetchall()
	output['unrelevant'] = len(this_duplicated)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='eliminated'")
	this_eliminated = cur.fetchall()
	output['eliminated'] = len(this_eliminated)

	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_literature_eliminated', output = output)	



@app.route('/literature_review/<id>/io')
def literature_review_io(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_output', output = output)	
	

@app.route('/literature_review/<id>/rr')
def literature_review_rr(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row

	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	if(data[11]):	
		output['research'] = json.loads(data[11])
		cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
		related_papers = cur.fetchall()
		json_category_data = []
		for _ in related_papers:
			mykeyword = _[16].replace(" ,",",").replace(", ",",")
			split_keyword = mykeyword.split(",")
			for _mykeyword in split_keyword:
				for __ in split_keyword:
					if(_mykeyword != __):
						# json_category_data = json_category_data + '{ from:"'+ _mykeyword +'", to: "'+__+'"},'
						json_category_data.append([_mykeyword,__])

		edges = json_category_data

		# Create empty nodes and connections dictionaries
		nodes = {}
		connections = {}

		# Loop through the edges and add unique nodes and connections
		# Loop through the edges and add unique nodes and connections
		for edge in edges:
			# Check if the from node is the same as the to node
			if edge[0] == edge[1]:
				continue  # Skip this edge and move on to the next one

			# Check if the from node already exists
			if edge[0] not in nodes:
				nodes[edge[0]] = {'id': edge[0], 'label': edge[0], 'value': 1}
			else:
				nodes[edge[0]]['value'] += 1

			# Check if the to node already exists
			if edge[1] not in nodes:
				nodes[edge[1]] = {'id': edge[1], 'label': edge[1], 'value': 1}
			else:
				nodes[edge[1]]['value'] += 1

			# Increment the connection count if the connection exists for both from and to nodes
			if edge[0] in connections and edge[1] in connections:
				connections[edge[0]] += 1
				connections[edge[1]] += 1
			else:
				connections[edge[0]] = 1
				connections[edge[1]] = 1

		# Convert nodes dictionary to a list of dictionaries
		nodes_list = list(nodes.values())

		# Use k-means clustering to cluster the nodes based on their connections
		cluster_count = 5  # set the number of clusters
		nodes_matrix = np.array([[node['value']] for node in nodes_list])
		kmeans = KMeans(n_clusters=cluster_count, random_state=0).fit(nodes_matrix)
		clusters = kmeans.labels_

		# Assign a cluster ID to each node
		for i in range(len(nodes_list)):
			nodes_list[i]['group'] = clusters[i]

		# Convert nodes and edges data to JSON
		nodes_data = json.dumps(nodes_list, default=str)
		edges_data = json.dumps([{'from': edge[0], 'to': edge[1]} for edge in edges])

		output['research']['nodes_data'] = Markup(nodes_data)
		output['research']['edges_data'] = Markup(edges_data)

	else:
		output['research'] = data[11]
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_research_result', output = output)	

@app.route('/literature_review/<id>/ie')
def literature_review_ie(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor(buffered=True)
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
	research_map = '{ "class": "go.TreeModel","nodeDataArray": [{"key":0, "text":"'+research_title+'", "loc":"-202.63350000000025 94.32549999999998"},{"key":1, "parent":0, "text":"Introduction", "brush":"skyblue", "dir":"right", "loc":"241.48515234374975 78.82549999999998"},{"key":3, "parent":0, "text":"Literature Study", "brush":"palevioletred", "dir":"right", "loc":"241.48515234374975 104.82549999999998"},{"key":4, "parent":0, "text":"Research Methods", "brush":"coral", "dir":"right", "loc":"241.48515234374975 130.82549999999998"}]}'
	cur = conn.cursor(buffered=True)
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
	cur = conn.cursor(buffered=True)
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
	cur = conn.cursor(buffered=True)
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
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	cur.execute("delete from paragraph_tb where research_id="+id)
	conn.commit()
	cur.execute("delete from references_tb where research_id="+id)
	conn.commit()
	cur.execute("delete from slr_tb where research_id="+id)
	conn.commit()
	getOpenAPI = GetOpenAPI(id)
	getOpenAPI.start()
	getLibrary = GetLibrary(id)
	getLibrary.start()
	# return {'status': 'ok'}, 200
	return Response(json.dumps({'success':True}),status=200, mimetype='application/json')

@app.route('/api/automate_openai_literature', methods=['POST'])
@cross_origin()
def automate_openai_literature():
	data = request.get_json()
	id = data['id']
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	cur.execute("delete from paragraph_tb where research_id="+id)
	conn.commit()
	cur.execute("delete from references_tb where research_id="+id)
	conn.commit()
	getOpenAPI = GetOpenAPI(id)
	getOpenAPI.start()
	return Response(json.dumps({'success':True}),status=200, mimetype='application/json')

@app.route('/api/automate_openai_paper', methods=['POST'])
@cross_origin()
def automate_openai_paper():
	data = request.get_json()
	id = data['id']
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	cur.execute("delete from slr_tb where research_id="+id)
	conn.commit()
	getLibrary = GetLibrary(id)
	getLibrary.start()
	return Response(json.dumps({'success':True}),status=200, mimetype='application/json')

@app.route('/api/start_count_total', methods=['POST'])
@cross_origin()
def start_count_total():
	data = request.get_json()
	input_keyword = data['input_keyword']
	# getLibrary = GetLibraryTest(input_keyword)
	# getLibrary.start()

	options = uc.ChromeOptions() 
	options.add_argument('--headless')
	driver = uc.Chrome(service=Service(ChromeDriverManager().install()), use_subprocess=True, options=options) 
	keyword_search = input_keyword

	#ieee
	temp_ieee_search = "("+keyword_search.replace('("','("Document Title":"').replace(' "',' "Document Title":"')+")"
	ieee_search = temp_ieee_search+" OR "+temp_ieee_search.replace("Document Title","Abstract")+" OR "+temp_ieee_search.replace("Document Title","Index Terms")
	ieee_search = ieee_search.replace(' ','%20')
	url_conference = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=("+ieee_search+")&highlight=true&returnType=SEARCH&matchPubs=true&rowsPerPage=100&refinements=ContentType:Conferences&refinements=ContentType:Journals&returnFacets=ALL"
	driver.get(url_conference)
	time.sleep(5)
	total_ieee = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]')
	total_document_ieee = total_ieee.text.split("of ")[1].split(" ")[0].replace(",","")
	# print(total_document_ieee)

	#sd
	sciencedirect_search = keyword_search.replace("(","%28").replace(" ","%20").replace(")","%29")
	url_sciencedirect = 'https://www.sciencedirect.com/search?tak='+sciencedirect_search+'&show=100&articleTypes=REV%2CFLA&lastSelectedFacet=articleTypes'
	driver.get(url_sciencedirect)
	time.sleep(5)
	total_document_sd = driver.find_element(By.CLASS_NAME,"ResultsFound").text.split(" ")[0].replace(",","")
	# print(total_document_sd)

	#acm
	temp_acm_search = "(Title:("+keyword_search+"))"
	temp_acm_search = temp_acm_search+" OR "+temp_acm_search.replace("Title","Abstract")+" OR "+temp_acm_search.replace("Title","Keyword")
	acm_search = temp_acm_search.replace('(','%28').replace(":","%3A").replace('"',"%22").replace(" ","+").replace(')','%29')
	url_acm = "https://dl.acm.org/action/doSearch?AllField="+acm_search+"&pageSize=100"
	driver.get(url_acm) 
	time.sleep(5)
	total_document_acm = driver.find_element(By.CLASS_NAME,"hitsLength").text.replace(",","")
	# print(total_document_acm)

	output_search = {
		'ieee' : total_document_ieee,
		'sciencedirect' : total_document_sd,
		'acm' : total_document_acm
	}
	return Response(json.dumps({'success':True, 'data':output_search}),status=200, mimetype='application/json')


##TESTING PAGE
# @app.route('/testing')
# def testing():
# 	keyword = "Cryptograhpy"
# 	google(keyword)

@app.route('/literature_review/slr/eliminated',methods = ['POST'])
@cross_origin()
def literature_review_slr_eliminated():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['slr_id']
	cur.execute('UPDATE slr_tb SET relevant=%s WHERE id=%s',['eliminated',id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/slr/related',methods = ['POST'])
@cross_origin()
def literature_review_slr_related():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['slr_id']
	cur.execute('UPDATE slr_tb SET relevant=%s WHERE id=%s',['related',id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/slr/unrelated',methods = ['POST'])
@cross_origin()
def literature_review_slr_unrelated():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['slr_id']
	cur.execute('UPDATE slr_tb SET relevant=%s WHERE id=%s',['unrelated',id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/slr/save_review',methods = ['POST'])
@cross_origin()
def literature_review_slr_save_review():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['slr_id']
	resume = data['resume']
	keyword = data['keyword']
	cur.execute('UPDATE slr_tb SET resume=%s,keyword=%s WHERE id=%s',[resume, keyword.lower().replace(";",","),id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')

@app.route('/literature_review/slr/result_crawling',methods = ['POST'])
@cross_origin()
def literature_review_slr_result_crawling():
	# print("berhasil")
	output = {}
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['research_id']
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()

	output['data'] = data
	keyword_search = data[6]

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()

	## START HERE
	
	result_keyword = {}
	result_keyword['original'] = keyword_search
	
	ieee_keyword_search = "("+keyword_search+")"
	temp_ieee_search = ieee_keyword_search.replace('("','("Document Title":"').replace(' "',' "Document Title":"')
	ieee_search = temp_ieee_search+" OR "+temp_ieee_search.replace("Document Title","Abstract")+" OR "+temp_ieee_search.replace("Document Title","Index Terms")
	result_keyword['ieee'] = ieee_search
	
	temp_acm_search = "(Title:("+keyword_search+"))"
	acm_search = temp_acm_search+" OR "+temp_acm_search.replace("Title","Abstract")+" OR "+temp_acm_search.replace("Title","Keyword")
	result_keyword['acm'] = acm_search


	result_keyword['sciencedirect'] = keyword_search


	options = uc.ChromeOptions() 
	options.add_argument('--headless')
	driver = uc.Chrome(service=Service(ChromeDriverManager().install()), use_subprocess=True, options=options) 

	## THIS IS IEEE
	temp_ieee_search = "("+keyword_search.replace('("','("Document Title":"').replace(' "',' "Document Title":"')+")"
	ieee_search = temp_ieee_search+" OR "+temp_ieee_search.replace("Document Title","Abstract")+" OR "+temp_ieee_search.replace("Document Title","Index Terms")
	ieee_search = ieee_search.replace(' ','%20')

	## IEEE BEFORE FILTER
	url_conference = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=("+ieee_search+")"
	driver.get(url_conference)
	time.sleep(5)
	total_ieee = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]')
	step_1_ieee = total_ieee.text.split("of ")[1].split(" ")[0].replace(",","")

	## IEEE AFTER FILTER
	url_conference = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=("+ieee_search+")&highlight=true&returnType=SEARCH&matchPubs=true&rowsPerPage=100&refinements=ContentType:Conferences&refinements=ContentType:Journals&returnFacets=ALL"
	driver.get(url_conference)
	time.sleep(5)
	total_ieee = driver.find_element(By.XPATH, '//*[@id="xplMainContent"]/div[1]/div[2]/xpl-search-dashboard/section/div/h1/span[1]')
	total_document_ieee = total_ieee.text.split("of ")[1].split(" ")[0].replace(",","")
	step_2_ieee = total_document_ieee

	#sd
	sciencedirect_search = keyword_search.replace("(","%28").replace(" ","%20").replace(")","%29")
	
	## SD BEFORE 
	url_sciencedirect = 'https://www.sciencedirect.com/search?tak='+sciencedirect_search
	driver.get(url_sciencedirect)
	time.sleep(5)
	step_1_sd = driver.find_element(By.CLASS_NAME,"ResultsFound").text.split(" ")[0].replace(",","")

	## SD AFLTER FILTER
	url_sciencedirect = 'https://www.sciencedirect.com/search?tak='+sciencedirect_search+'&show=100&articleTypes=REV%2CFLA&lastSelectedFacet=articleTypes'
	driver.get(url_sciencedirect)
	time.sleep(5)
	total_document_sd = driver.find_element(By.CLASS_NAME,"ResultsFound").text.split(" ")[0].replace(",","")
	step_2_sd = total_document_sd
	# print(total_document_sd)

	#acm
	temp_acm_search = "(Title:("+keyword_search+"))"
	temp_acm_search = temp_acm_search+" OR "+temp_acm_search.replace("Title","Abstract")+" OR "+temp_acm_search.replace("Title","Keyword")
	acm_search = temp_acm_search.replace('(','%28').replace(":","%3A").replace('"',"%22").replace(" ","+").replace(')','%29')

	## ACM AFTER
	url_acm = "https://dl.acm.org/action/doSearch?AllField="+acm_search+"&pageSize=100"
	driver.get(url_acm) 
	time.sleep(5)
	step_1_acm = driver.find_element(By.CLASS_NAME,"hitsLength").text.replace(",","")
	step_2_acm = step_1_acm
	# print(total_document_acm)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='duplicated'")
	related_papers = cur.fetchall()

	step_3_ieee_min = 0
	step_3_sd_min = 0
	step_3_acm_min = 0

	for _ in related_papers:
		if(_[11] == "IEEE"):
			step_3_ieee_min = step_3_ieee_min+1
		if(_[11] == "Sciencedirect"):
			step_3_sd_min = step_3_sd_min+1
		if(_[11] == "ACM Digital Library"):
			step_3_acm_min = step_3_acm_min+1

	step_3_ieee = int(step_2_ieee) - step_3_ieee_min
	step_3_sd = int(step_2_sd) - step_3_sd_min
	step_3_acm = int(step_2_acm) - step_3_acm_min

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()

	step_5_ieee = 0
	step_5_sd = 0
	step_5_acm = 0

	for _ in related_papers:
		if(_[11] == "IEEE"):
			step_5_ieee = step_5_ieee+1
		if(_[11] == "Sciencedirect"):
			step_5_sd = step_5_sd+1
		if(_[11] == "ACM Digital Library"):
			step_5_acm = step_5_acm+1
	
	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='eliminated'")
	related_papers = cur.fetchall()

	step_4_ieee_min = 0
	step_4_sd_min = 0
	step_4_acm_min = 0

	for _ in related_papers:
		if(_[11] == "IEEE"):
			step_4_ieee_min = step_4_ieee_min+1
		if(_[11] == "Sciencedirect"):
			step_4_sd_min = step_4_sd_min+1
		if(_[11] == "ACM Digital Library"):
			step_4_acm_min = step_4_acm_min+1

	step_4_ieee = int(step_5_ieee) + step_4_ieee_min
	step_4_sd = int(step_5_sd) + step_4_sd_min
	step_4_acm = int(step_5_acm) + step_4_acm_min

	per_stages = {}

	per_stages['IEEE'] = {
		"Stage 1":step_1_ieee,"Stage 2":step_2_ieee,"Stage 3":step_3_ieee,"Stage 4":step_4_ieee,"Stage 5":step_5_ieee
	}
	per_stages['Science Direct'] = {
		"Stage 1":step_1_sd,"Stage 2":step_2_sd,"Stage 3":step_3_sd,"Stage 4":step_4_sd,"Stage 5":step_5_sd
	}
	per_stages['ACM Digital Library'] = {
		"Stage 1":step_1_acm,"Stage 2":step_2_acm,"Stage 3":step_3_acm,"Stage 4":step_4_acm,"Stage 5":step_5_acm
	}
	per_stages['all'] = {
		"Stage 1":int(step_1_ieee)+int(step_1_sd)+int(step_1_acm),"Stage 2":int(step_2_ieee)+int(step_2_sd)+int(step_2_acm),"Stage 3":int(step_3_ieee)+int(step_3_sd)+int(step_3_acm),"Stage 4":int(step_4_ieee)+int(step_4_sd)+int(step_4_acm),"Stage 5":int(step_5_ieee)+int(step_5_sd)+int(step_5_acm)
	}

	per_year = {}
	list_year = []

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()
	my_year = [_[6]for _ in related_papers]
	my_year.sort()
	my_dict = {i:my_year.count(i) for i in my_year}
	per_year['all'] = my_dict 

	for _ in my_dict:
		list_year.append(_)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related' AND source='IEEE'")
	related_papers = cur.fetchall()
	my_year = [_[6]for _ in related_papers]
	my_year.sort()
	my_dict = {i:my_year.count(i) for i in my_year}
	per_year['IEEE'] = my_dict 

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related' AND source='Sciencedirect'")
	related_papers = cur.fetchall()
	my_year = [_[6]for _ in related_papers]
	my_year.sort()
	my_dict = {i:my_year.count(i) for i in my_year}
	per_year['Sciencedirect'] = my_dict 

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related' AND source='ACM Digital Library'")
	related_papers = cur.fetchall()
	my_year = [_[6]for _ in related_papers]
	my_year.sort()
	my_dict = {i:my_year.count(i) for i in my_year}
	per_year['ACM Digital Library'] = my_dict 

	per_years = {}
	per_years['data'] = per_year
	per_years['year'] = list_year

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()

	per_publisher = {}
	per_publisher_ieee = 0
	per_publisher_sd = 0
	per_publisher_acm = 0

	for _ in related_papers:
		if(_[11] == "IEEE"):
			per_publisher_ieee = per_publisher_ieee+1
		if(_[11] == "Sciencedirect"):
			per_publisher_sd = per_publisher_sd+1
		if(_[11] == "ACM Digital Library"):
			per_publisher_acm = per_publisher_acm+1

	per_publisher['all'] = int(per_publisher_ieee)+int(per_publisher_sd)+int(per_publisher_acm)
	per_publisher['IEEE'] = int(per_publisher_ieee)
	per_publisher['Sciencedirect'] = int(per_publisher_sd)
	per_publisher['ACM Digital Library'] = int(per_publisher_acm)

	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()
	all_publisher = [_[5]for _ in related_papers]
	all_publisher.sort()
	related_publisher = {i:all_publisher.count(i) for i in all_publisher}

	_publisher = {}

	_citiedby = []

	for _temp in related_publisher:
		# print(_temp)
		cur.execute("select * from slr_tb where research_id=%s AND event=%s AND relevant='related'",[id,_temp])
		related_papers = cur.fetchall()
		no = 0

		cur.execute("select * from scimago_tb where Title=%s",[_temp])
		related_scimago = cur.fetchone()

		# print(related_scimago)
		_publisher[_temp] = {}
		for __ in related_papers:
			_data = {}
			_data['scimago'] = related_scimago
			_data['title'] = __[2]
			_data['author'] = __[4]
			_data['year'] = __[6]
			_data['keyword'] = __[16]
			_data['source'] = __[11]
			_data['citied'] = __[17]
			_mc = {}
			_mc['title'] = __[2]
			_mc['author'] = __[4]
			_mc['year'] = __[6]
			_mc['keyword'] = __[16]
			_mc['citied'] = int(__[17])
			_mc['source'] = __[11]
			_publisher[_temp][no] = _data
			_citiedby.append(_mc)
			no=no+1
	

	_sci = []
	for _temp in related_publisher:
		# print(_temp)
		cur.execute("select * from scimago_tb where Title=%s",[_temp])
		related_scimago = cur.fetchone()
		if(related_scimago is not None):
			data =  {}
			data['Title'] = related_scimago[2]
			data['SJR'] = related_scimago[5]
			data['H_index'] = related_scimago[7]
			data['Total_Doc'] = related_scimago[8]
			data['Total_Ref'] = related_scimago[9]
			data['Total_Cities'] = related_scimago[10]
			data['Total_Citied'] = related_scimago[11]
			data['Country'] = related_scimago[15]
			data['Region'] = related_scimago[16]
			data['Publisher'] = related_scimago[17]
			# print(data)
			_sci.append(data)
	
	# print(_sci)
	if(len(_sci) > 0):
		scimagojr = pd.DataFrame(_sci)
		scimagojr = scimagojr.sort_values(by=['SJR'], ascending=False)
		
		per_scimagojr = scimagojr.to_json(orient="split")
		per_scimagojr = json.loads(per_scimagojr)

		citiedby = pd.DataFrame(_citiedby)
		citiedby = citiedby.sort_values(by=['citied'], ascending=False)
		
		per_citiedby = citiedby.to_json(orient="split")
		per_citiedby = json.loads(per_citiedby)
	else:
		per_scimagojr = {}
		per_citiedby = {}

	##DATA PERKEYWORD
	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()
	all_category_data = []
	json_category_data = ""
	for _ in related_papers:
		mykeyword = _[16].replace(" ,",",").replace(", ",",")
		split_keyword = mykeyword.split(",")
		for _mykeyword in split_keyword:
			all_category_data.append(_mykeyword)
			# for __ in split_keyword:
			# 	if(all_category_data != __):
			# 		json_category_data = json_category_data + '{ from:"'+ all_category_data +'", to: "'+__+'"},'


	per_keyword = {i:all_category_data.count(i) for i in all_category_data}	
	data_per_keyword = []
	for _ in per_keyword:
		temp = {}
		temp['keyword'] = _
		temp['value'] = per_keyword[_]
		data_per_keyword.append(temp)

	if(len(data_per_keyword) > 0):
		data_per_keyword = pd.DataFrame(data_per_keyword)
		data_per_keyword = data_per_keyword.sort_values(by=['value'], ascending=False)
		
		data_per_keyword = data_per_keyword.to_json(orient="split")
		data_per_keyword = json.loads(data_per_keyword)
	else:
		data_per_keyword = {}


	##DATA PER AUTHOR
	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()
	all_category_data_author = []
	# print("get author name")
	for _ in related_papers:
		myauthor = _[4].replace(" ;",";").replace("; ",";")
		# print(myauthor)
		split_myauthor = myauthor.split(";")
		for _myauthor in split_myauthor:
			all_category_data_author.append(_myauthor)
	# print("get author cat")
	per_author = {i:all_category_data_author.count(i) for i in all_category_data_author}	
	print(per_author)
	data_per_author = []
	for _ in per_author:
		temp = {}
		temp['author'] = _
		temp['value'] = per_author[_]
		data_per_author.append(temp)
	# print("get per data author")
	# print(data_per_author)
	if(len(data_per_author) > 0):
		data_per_author = pd.DataFrame(data_per_author)
		data_per_author = data_per_author.sort_values(by=['value'], ascending=False)
		
		data_per_author = data_per_author.to_json(orient="split")
		data_per_author = json.loads(data_per_author)
	else:
		# print("tidak ada data")
		data_per_author = {}

	this_output = {}
	this_output['result_keyword'] = result_keyword
	this_output['per_stages'] = per_stages
	this_output['per_year'] = per_years
	this_output['per_publisher'] = per_publisher
	this_output['per_journal'] = _publisher
	this_output['per_scimagojr'] = per_scimagojr
	this_output['per_citiedby'] = per_citiedby
	this_output['per_keyword'] = data_per_keyword
	this_output['per_author'] = data_per_author
	

	# END HERE
	cur.execute('UPDATE research_slr SET summary=%s WHERE id=%s',[json.dumps(this_output),id])
	conn.commit()

	return Response(json.dumps(this_output),status=200, mimetype='application/json')


@app.route('/literature_review/slr/generate_research',methods = ['POST'])
@cross_origin()
def literature_review_generate_research():

	"""
	text_header => <h2><strong>Implementation Big Data For National Security and Intelligence Agency</strong></h2><hr />
	text_author => <p><strong>Author:</strong></p><p>Rizqy Rionaldy</p><hr />
	text_abstract => <p><strong>Abstract:</strong></p><p>&nbsp;</p><hr />
	text_introduction => <p><strong>Introduction:</strong></p><p>&nbsp;</p><hr />
	text_literature => <p><strong>Literature Review:</strong></p><p>&nbsp;</p><hr />
	text_methods => <p><strong>Research Methods:</strong></p><p>&nbsp;</p><hr />
	text_result => <p><strong>Result:</strong></p><p>&nbsp;</p><hr />
	text_discussion => <p><strong>Discussion:</strong></p><p>&nbsp;</p><hr />
	text_conclusion => <p><strong>Conclusion:</strong></p><p>&nbsp;</p><hr />
	text_references => <p><strong>References:</strong></p><p>&nbsp;</p>
	text_paper => all
	"""
	
	output = {}
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	data = request.get_json()
	id = data['research_id']
	cur.execute("select * from research_slr where id="+id)
	research_slr = cur.fetchone()

	text_header = "<h2><strong>"+research_slr[1]+"</strong></h2><hr />"
	text_author = "<p><strong>Author:</strong></p><p>"+research_slr[2]+"</p><hr />"
	text_abstract = "<p><strong>Abstract:</strong></p><p>&nbsp;</p><hr />"

	##############
	#INTRODUCTION#
	##############
	cur.execute("select paragraph_json from paragraph_tb where research_id="+id+" AND category='introduction'")
	paragraph_tb_introduction = cur.fetchone()
	paragraph_tb_introduction = json.loads(paragraph_tb_introduction[0])
	text_introduction = "<p><strong>Introduction:</strong></p><p>"
	for _per in paragraph_tb_introduction:
		text_introduction = text_introduction + str(paragraph_tb_introduction[_per])
	text_introduction = text_introduction+"</p><hr />"


	##############
	#LITERATURE#
	##############
	cur.execute("select paragraph_json from paragraph_tb where research_id="+id+" AND category='literature'")
	paragraph_tb_literature = cur.fetchone()
	paragraph_tb_literature = json.loads(paragraph_tb_literature[0])
	text_literature = "<p><strong>Literature Review:</strong></p><p>"
	for _per in paragraph_tb_literature:
		text_literature = text_literature + str(paragraph_tb_literature[_per])
	text_literature = text_literature+"</p><hr />"


	##############
	#METHODS#
	##############
	cur.execute("select paragraph_json from paragraph_tb where research_id="+id+" AND category='methodology'")
	paragraph_tb_methodology = cur.fetchone()
	paragraph_tb_methodology = json.loads(paragraph_tb_methodology[0])
	text_methodology = "<p><strong>Research Methods:</strong></p><p>"
	for _per in paragraph_tb_methodology:
		text_methodology = text_methodology + str(paragraph_tb_methodology[_per])
	text_methodology = text_methodology+"</p><hr />"



	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()

	## UPDATE DATABASE
	text_paper = text_header+text_author+text_abstract+text_introduction+text_literature+text_methodology
	cur.execute('UPDATE research_slr SET output=%s WHERE id=%s',[text_paper,id])
	conn.commit()
	
	return Response(json.dumps(research_slr),status=200, mimetype='application/json')

	## START HERE

@app.route('/literature_review/<id>/bb')
def literature_review_bb(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row

	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	if(data[11]):	
		output['research'] = {}
		cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
		related_papers = cur.fetchall()
		json_category_data = []
		for _ in related_papers:
			mykeyword = _[16].replace(" ,",",").replace(", ",",")
			split_keyword = mykeyword.split(",")
			for _mykeyword in split_keyword:
				for __ in split_keyword:
					if(_mykeyword != __):
						# json_category_data = json_category_data + '{ from:"'+ _mykeyword +'", to: "'+__+'"},'
						json_category_data.append([_mykeyword,__])

		edges = json_category_data

		# Create empty nodes and connections dictionaries
		nodes = {}
		connections = {}

		# Loop through the edges and add unique nodes and connections
		# Loop through the edges and add unique nodes and connections
		for edge in edges:
			# Check if the from node is the same as the to node
			if edge[0] == edge[1]:
				continue  # Skip this edge and move on to the next one

			# Check if the from node already exists
			if edge[0] not in nodes:
				nodes[edge[0]] = {'id': edge[0], 'label': edge[0], 'value': 1}
			else:
				nodes[edge[0]]['value'] += 1

			# Check if the to node already exists
			if edge[1] not in nodes:
				nodes[edge[1]] = {'id': edge[1], 'label': edge[1], 'value': 1}
			else:
				nodes[edge[1]]['value'] += 1

			# Increment the connection count if the connection exists for both from and to nodes
			if edge[0] in connections and edge[1] in connections:
				connections[edge[0]] += 1
				connections[edge[1]] += 1
			else:
				connections[edge[0]] = 1
				connections[edge[1]] = 1

		# Convert nodes dictionary to a list of dictionaries
		nodes_list = list(nodes.values())

		# Use k-means clustering to cluster the nodes based on their connections
		cluster_count = 5  # set the number of clusters
		nodes_matrix = np.array([[node['value']] for node in nodes_list])
		kmeans = KMeans(n_clusters=cluster_count, random_state=0).fit(nodes_matrix)
		clusters = kmeans.labels_

		# Assign a cluster ID to each node
		for i in range(len(nodes_list)):
			nodes_list[i]['group'] = clusters[i]

		# Convert nodes and edges data to JSON
		nodes_data = json.dumps(nodes_list, default=str)
		edges_data = json.dumps([{'from': edge[0], 'to': edge[1]} for edge in edges])

		output['research']['nodes_data'] = Markup(nodes_data)
		output['research']['edges_data'] = Markup(edges_data)

	else:
		output['research'] = data[11]
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_bibliometric_keyword', output = output)	



@app.route('/literature_review/<id>/bb_resume')
def literature_review_bb_resume(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row

	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	if(data[11]):	
		output['research'] = {}
		cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
		related_papers = cur.fetchall()
		json_category_data = []
		for _ in related_papers:
			mykeyword = _[4].replace(" ;",";").replace("; ",";")
			split_keyword = mykeyword.split(";")
			for _mykeyword in split_keyword:
				for __ in split_keyword:
					if(_mykeyword != __):
						# json_category_data = json_category_data + '{ from:"'+ _mykeyword +'", to: "'+__+'"},'
						json_category_data.append([_mykeyword,__])

		edges = json_category_data

		# Create empty nodes and connections dictionaries
		nodes = {}
		connections = {}

		# Loop through the edges and add unique nodes and connections
		# Loop through the edges and add unique nodes and connections
		for edge in edges:
			# Check if the from node is the same as the to node
			if edge[0] == edge[1]:
				continue  # Skip this edge and move on to the next one

			# Check if the from node already exists
			if edge[0] not in nodes:
				nodes[edge[0]] = {'id': edge[0], 'label': edge[0], 'value': 1}
			else:
				nodes[edge[0]]['value'] += 1

			# Check if the to node already exists
			if edge[1] not in nodes:
				nodes[edge[1]] = {'id': edge[1], 'label': edge[1], 'value': 1}
			else:
				nodes[edge[1]]['value'] += 1

			# Increment the connection count if the connection exists for both from and to nodes
			if edge[0] in connections and edge[1] in connections:
				connections[edge[0]] += 1
				connections[edge[1]] += 1
			else:
				connections[edge[0]] = 1
				connections[edge[1]] = 1

		# Convert nodes dictionary to a list of dictionaries
		nodes_list = list(nodes.values())

		# Use k-means clustering to cluster the nodes based on their connections
		cluster_count = 5  # set the number of clusters
		nodes_matrix = np.array([[node['value']] for node in nodes_list])
		kmeans = KMeans(n_clusters=cluster_count, random_state=0).fit(nodes_matrix)
		clusters = kmeans.labels_

		# Assign a cluster ID to each node
		for i in range(len(nodes_list)):
			nodes_list[i]['group'] = clusters[i]

		# Convert nodes and edges data to JSON
		nodes_data = json.dumps(nodes_list, default=str)
		edges_data = json.dumps([{'from': edge[0], 'to': edge[1]} for edge in edges])

		output['research']['nodes_data'] = Markup(nodes_data)
		output['research']['edges_data'] = Markup(edges_data)

		
		# BAR CHART
		barWidth = 0.25
		fig, ax = plt.subplots(figsize=(8, 6))
				
		# set height of bar
		IT = [12, 30, 1, 8, 22]
		ECE = [28, 6, 16, 5, 10]
		CSE = [29, 3, 24, 25, 17]
				
		# Set position of bar on X axis
		br1 = np.arange(len(IT))
		br2 = [x + barWidth for x in br1]
		br3 = [x + barWidth for x in br2]
				
		# Make the plot
		ax.bar(br1, IT, color='orange', width=barWidth, edgecolor='grey', label='IT')
		ax.bar(br2, ECE, color='g', width=barWidth, edgecolor='grey', label='ECE')
		ax.bar(br3, CSE, color='b', width=barWidth, edgecolor='grey', label='CSE')

		# Adding label values
		for i, v in enumerate(IT):
			ax.text(i - 0.1, v + 0.5, str(v), color='black', fontweight='bold')
		for i, v in enumerate(ECE):
			ax.text(i + 0.15, v + 0.5, str(v), color='black', fontweight='bold')
		for i, v in enumerate(CSE):
			ax.text(i + 0.4, v + 0.5, str(v), color='black', fontweight='bold')
				
		# Adding Xticks
		ax.set_xlabel('Branch', fontweight='bold', fontsize=15)
		ax.set_ylabel('Students passed', fontweight='bold', fontsize=15)
		ax.set_xticks([r + barWidth for r in range(len(IT))])
		ax.set_xticklabels(['2015', '2016', '2017', '2018', '2019'])

		ax.legend()

		# Export the plot to HTML using mpld3
		html_str = mpld3.fig_to_html(fig)
		bar_chart = Markup(html_str)
		output['research']['barplot'] = bar_chart

		plt.clf()

		# Create a pie chart
		labels= ['Mortgage', 'Utilities', 'Food']
		colors=['orange', 'green', 'blue']
		sizes= [1500, 600, 500]

		# Set default font size and style
		plt.rcParams.update({'font.size': 16, 'font.family': 'serif'})

		# Create pie chart with centered label text
		plt.pie(sizes, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%', textprops={'horizontalalignment':'center', 'verticalalignment':'center'})

		plt.axis('equal')

		html_str = mpld3.fig_to_html(plt.gcf())

		pie_chart = Markup(html_str)
		output['research']['piechart'] = pie_chart

		# First treemap
		plt.clf()
		# Create a data frame with fake data
		df1 = pd.DataFrame({'nb_people':[8, 5, 3, 2, 1], 'group':["Group A", "Group B", "Group C", "Group D", "Group E"] })

		# plot it
		squarify.plot(sizes=df1['nb_people'], label=df1['group'], alpha=.8 )
		plt.axis('off')
		html_str_1 = mpld3.fig_to_html(plt.gcf())
		treemap_chart_1 = Markup(html_str_1)

		# Second treemap
		plt.clf()
		# Create a data frame with fake data
		df2 = pd.DataFrame({'nb_people':[10, 8, 5, 3, 1], 'group':["Group E", "Group C", "Group A", "Group B", "Group D"] })

		# plot it
		squarify.plot(sizes=df2['nb_people'], label=df2['group'], alpha=.8 )
		plt.axis('off')
		html_str_2 = mpld3.fig_to_html(plt.gcf())
		treemap_chart_2 = Markup(html_str_2)

		output['research']['author'] = treemap_chart_1
		output['research']['keyword'] = treemap_chart_2

		# Convert the figure to an SVG string
		svg_io = io.StringIO()
		mpld3.save_html(plt.gcf(), svg_io)
		svg_string = svg_io.getvalue()
		output['research']['keyword_string'] = svg_string

	else:
		output['research'] = data[11]
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_bibliometric_resume', output = output)	


@app.route('/literature_review/<id>/bb_author')
def literature_review_bb_author(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row

	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	if(data[11]):	
		output['research'] = {}
		cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
		related_papers = cur.fetchall()
		json_category_data = []
		for _ in related_papers:
			mykeyword = _[4].replace(" ;",";").replace("; ",";")
			split_keyword = mykeyword.split(";")
			for _mykeyword in split_keyword:
				for __ in split_keyword:
					if(_mykeyword != __):
						# json_category_data = json_category_data + '{ from:"'+ _mykeyword +'", to: "'+__+'"},'
						json_category_data.append([_mykeyword,__])

		edges = json_category_data

		# Create empty nodes and connections dictionaries
		nodes = {}
		connections = {}

		# Loop through the edges and add unique nodes and connections
		# Loop through the edges and add unique nodes and connections
		for edge in edges:
			# Check if the from node is the same as the to node
			if edge[0] == edge[1]:
				continue  # Skip this edge and move on to the next one

			# Check if the from node already exists
			if edge[0] not in nodes:
				nodes[edge[0]] = {'id': edge[0], 'label': edge[0], 'value': 1}
			else:
				nodes[edge[0]]['value'] += 1

			# Check if the to node already exists
			if edge[1] not in nodes:
				nodes[edge[1]] = {'id': edge[1], 'label': edge[1], 'value': 1}
			else:
				nodes[edge[1]]['value'] += 1

			# Increment the connection count if the connection exists for both from and to nodes
			if edge[0] in connections and edge[1] in connections:
				connections[edge[0]] += 1
				connections[edge[1]] += 1
			else:
				connections[edge[0]] = 1
				connections[edge[1]] = 1

		# Convert nodes dictionary to a list of dictionaries
		nodes_list = list(nodes.values())

		# Use k-means clustering to cluster the nodes based on their connections
		cluster_count = 5  # set the number of clusters
		nodes_matrix = np.array([[node['value']] for node in nodes_list])
		kmeans = KMeans(n_clusters=cluster_count, random_state=0).fit(nodes_matrix)
		clusters = kmeans.labels_

		# Assign a cluster ID to each node
		for i in range(len(nodes_list)):
			nodes_list[i]['group'] = clusters[i]

		# Convert nodes and edges data to JSON
		nodes_data = json.dumps(nodes_list, default=str)
		edges_data = json.dumps([{'from': edge[0], 'to': edge[1]} for edge in edges])

		output['research']['nodes_data'] = Markup(nodes_data)
		output['research']['edges_data'] = Markup(edges_data)

	else:
		output['research'] = data[11]
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_bibliometric_author', output = output)	




app.run(host="0.0.0.0", debug = True) if __name__ == '__main__' else "Error"
