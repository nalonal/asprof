from function import *

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
	cur.execute("select * from research_slr ORDER BY id desc")
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
	

@app.route('/literature_review/<id>/html')
def literature_review_html(id):
	output = {}
	id = id
	conn = dbcon()
	title = 'Systematic Literature Review'
	# conn.row_factory = sql.Row
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	output['data'] = data
	output['html'] = Markup(data[8])
	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_html', output = output)	
	


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
	research_slr_html = json.loads(research_slr[15])

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
	text_methodology = text_methodology+research_slr_html['table_result_keyword']
	text_methodology = text_methodology+research_slr_html['diagram_flowchart']+'<br>'
	text_methodology = text_methodology+research_slr_html['table_per_stages']+'<br>'
	text_methodology = text_methodology+research_slr_html['table_per_year_paper']+'<br>'
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
			try:
				mykeyword = _[16].replace(" ,",",").replace(", ",",")
				split_keyword = mykeyword.split(",")
				for _mykeyword in split_keyword:
					for __ in split_keyword:
						if(_mykeyword != __):
							# unidecode(_mykeyword.lower())
							# json_category_data = json_category_data + '{ from:"'+ _mykeyword +'", to: "'+__+'"},'
							json_category_data.append([unidecode(_mykeyword.lower()),unidecode(__.lower())])
			except:
				pass

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
		get_data = json.loads(data[11])
		flowchart_params_1 = get_data["per_stages"]['all']['Stage 1']
		flowchart_params_2 = get_data["per_stages"]['all']['Stage 2'] - get_data["per_stages"]['all']['Stage 3']
		flowchart_params_3 = get_data["per_stages"]['all']['Stage 3']
		flowchart_params_4 = get_data["per_stages"]['all']['Stage 3'] - get_data["per_stages"]['all']['Stage 4']
		flowchart_params_5 = get_data["per_stages"]['all']['Stage 4']
		flowchart_params_6 = get_data["per_stages"]['all']['Stage 4'] - get_data["per_stages"]['all']['Stage 5']
		flowchart_params_7 = get_data["per_stages"]['all']['Stage 5']
		string_flowchart = '{ "class": "go.GraphLinksModel", "linkFromPortIdProperty": "fromPort", "linkToPortIdProperty": "toPort", "nodeDataArray": [ {"key":-11, "loc":"164 85.99999999999996", "text":"Titles/abstracts screened (n='+str(flowchart_params_3)+')"}, {"key":-4, "loc":"422.00000000000034 86.00000000000006", "text":"Exluded (n='+str(flowchart_params_4)+') Inaccessible, Irrelevant"}, {"key":-5, "loc":"164.00000000000003 159.9999999999999", "text":"Full-text articles assessed for Eligibility (n='+str(flowchart_params_5)+')"}, {"key":-6, "loc":"-73 164", "category":"Yellowish", "text":"Eligibility"}, {"key":-7, "loc":"-77.00000000000017 45.99999999999994", "category":"Yellowish", "text":"Screening"}, {"key":-8, "loc":"-78.00000000000003 -76.99999999999986", "category":"Yellowish", "text":"Identification"}, {"key":-9, "loc":"-73.99999999999994 244.99999999999972", "category":"Yellowish", "text":"Included"}, {"key":-10, "loc":"421.9999999999998 159.9999999999999", "text":"Full-text articles excluded (n='+str(flowchart_params_6)+')"}, {"key":-12, "loc":"164.00000000000003 250.0000000000001", "text":"Studies included for qualitative and quantitative analysis and synthesis (n='+str(flowchart_params_7)+')"}, {"key":-3, "loc":"164.00000000000006 14", "text":"Records after duplicates removed (n='+str(flowchart_params_3)+')"}, {"key":-13, "loc":"164.00000000000006 -79", "text":"Electronic Database Searches : IEEE, ScienceDirect, ACM Digital Library (n='+str(flowchart_params_1)+')"} ], "linkDataArray": [ {"from":-5, "to":-10, "fromPort":"R", "toPort":"L", "points":[264.5,159.9999999999999,274.5,159.9999999999999,292.9999999999999,159.9999999999999,292.9999999999999,159.9999999999999,311.4999999999998,159.9999999999999,321.4999999999998,159.9999999999999]}, {"from":-5, "to":-12, "fromPort":"B", "toPort":"T", "points":[164.00000000000003,187.99238281249987,164.00000000000003,197.99238281249987,164.00000000000003,201.75126953125,164.00000000000003,201.75126953125,164.00000000000003,205.5101562500001,164.00000000000003,215.5101562500001]}, {"from":-3, "to":-11, "fromPort":"B", "toPort":"T", "points":[164.00000000000006,41.9923828125,164.00000000000006,51.9923828125,164.00000000000006,53.248730468749976,164,53.248730468749976,164,54.505078124999955,164,64.50507812499995]}, {"from":-11, "to":-4, "fromPort":"R", "toPort":"L", "points":[264.5,85.99999999999996,274.5,85.99999999999996,293.0000000000001,85.99999999999996,293.0000000000001,86.00000000000001,311.5000000000002,86.00000000000001,321.5000000000002,86.00000000000001]}, {"from":-13, "to":-3, "fromPort":"B", "toPort":"T", "points":[164.00000000000006,-38.0126953125,164.00000000000006,-28.0126953125,164.00000000000006,-26.0025390625,164.00000000000006,-26.0025390625,164.00000000000006,-23.9923828125,164.00000000000006,-13.9923828125]}, {"from":-11, "to":-5, "fromPort":"B", "toPort":"T", "points":[164,107.49492187499996,164,117.49492187499996,164,119.75126953124992,164.00000000000003,119.75126953124992,164.00000000000003,122.00761718749987,164.00000000000003,132.00761718749987]} ]}'
		output['research']= get_data
		output['research']['per_author']['data']= get_data['per_author']['data'][0:9]
		output['research']['per_keyword']['data']= get_data['per_keyword']['data'][0:9]
		# output['research']['diagram_flowchart'] = get_file_url(id,'diagram_flowchart')
		output['research']['diagram_per_year_paper'] = get_file_url(id,'diagram_per_year_paper')
		output['research']['diagram_per_year'] = get_file_url(id,'diagram_per_year')
		output['research']['diagram_per_source'] = get_file_url(id,'diagram_per_source')
		output['research']['diagram_per_author'] = get_file_url(id,'diagram_per_author')
		output['research']['diagram_per_keyword'] = get_file_url(id,'diagram_per_keyword')
		output['research']['diagram_sna_keyword'] = get_file_url(id,'diagram_sna_keyword')
		output['research']['string_flowchart'] = string_flowchart
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
						#unidecode(_mykeyword.lower())
						# json_category_data = json_category_data + '{ from:"'+ _mykeyword +'", to: "'+__+'"},'
						json_category_data.append([unidecode(_mykeyword.lower()),unidecode(__.lower())])

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

@app.route('/literature_review/slr/bibliometric_update_all',methods = ['POST'])
@cross_origin()
def literature_bibliometric_all():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	img_data = request.form['img_data'].split(',')[1]
	id = request.form['id']
	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()
	literature_review_slr_result_crawling(id)
	file_diagram_per_year_paper = diagram_per_year_paper(id)
	update_file(file_diagram_per_year_paper,id,"diagram_per_year_paper",".png")
	file_diagram_per_year = diagram_per_year(id)
	update_file(file_diagram_per_year,id,"diagram_per_year",".png")
	file_diagram_per_source = diagram_per_source(id)
	update_file(file_diagram_per_source,id,"diagram_per_source",".png")
	file_diagram_per_author = diagram_per_author(id)
	update_file(file_diagram_per_author,id,"diagram_per_author",".png")
	file_diagram_per_keyword = diagram_per_keyword(id)
	update_file(file_diagram_per_keyword,id,"diagram_per_keyword",".png")
	file_diagram_flowchart = io.BytesIO(base64.b64decode(img_data))
	file_diagram_flowchart.seek(0)
	update_file(file_diagram_flowchart,id,"diagram_flowchart",".png")
	summary_to_detail(id)
	return Response(json.dumps({'id':id}),status=200, mimetype='application/json')


@app.route('/literature_review/slr/bibliometric_update',methods = ['POST'])
@cross_origin()
def literature_bibliometric():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	img_data = request.form['img_data'].split(',')[1]
	id = request.form['id']
	cur.execute("select * from slr_tb where research_id="+id+" AND relevant='related'")
	related_papers = cur.fetchall()
	literature_review_slr_result_crawling(id)
	file_diagram_per_year_paper = diagram_per_year_paper(id)
	update_file(file_diagram_per_year_paper,id,"diagram_per_year_paper",".png")
	file_diagram_per_year = diagram_per_year(id)
	update_file(file_diagram_per_year,id,"diagram_per_year",".png")
	file_diagram_per_source = diagram_per_source(id)
	update_file(file_diagram_per_source,id,"diagram_per_source",".png")
	file_diagram_per_author = diagram_per_author(id)
	update_file(file_diagram_per_author,id,"diagram_per_author",".png")
	file_diagram_per_keyword = diagram_per_keyword(id)
	update_file(file_diagram_per_keyword,id,"diagram_per_keyword",".png")
	return Response(json.dumps({'id':id}),status=200, mimetype='application/json')

@app.route('/literature_review/slr/bibliometric_update_keyword',methods = ['POST'])
@cross_origin()
def literature_bibliometric_keyword():
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	img_data = request.form['img_data'].split(',')[1]
	id = request.form['id']
	file_diagram_flowchart = io.BytesIO(base64.b64decode(img_data))
	file_diagram_flowchart.seek(0)
	update_file(file_diagram_flowchart,id,"diagram_sna_keyword",".png")
	return Response(json.dumps({'id':id}),status=200, mimetype='application/json')

app.run(host="0.0.0.0", debug = True) if __name__ == '__main__' else "Error"
