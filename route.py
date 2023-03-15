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
	cur.execute('UPDATE research_slr SET research_title=%s, research_author=%s WHERE id=%s',[research_title,research_author,id])
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

	return render_template(setup.PATH_TEMPLATE, id = id, title=title, page='literature_review', view_file='index_literature_unrelated', output = output)	
	

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
	getOpenAPI = GetOpenAPI(id)
	getOpenAPI.start()
	getLibrary = GetLibrary(id)
	getLibrary.start()
	# return {'status': 'ok'}, 200
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
	cur.execute('UPDATE slr_tb SET resume=%s WHERE id=%s',[resume,id])
	conn.commit()
	return Response(json.dumps(data),status=200, mimetype='application/json')




app.run(host="0.0.0.0", debug = True) if __name__ == '__main__' else "Error"