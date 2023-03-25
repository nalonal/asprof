
from app import *


def summary_to_detail(id):
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	cur.execute("select * from research_slr where id="+id)
	data = cur.fetchone()
	get_data = json.loads(data[11])
	flowchart_params_1 = get_data["per_stages"]['all']['Stage 1']
	flowchart_params_2 = get_data["per_stages"]['all']['Stage 1']
	flowchart_params_3 = int(get_data["per_stages"]['all']['Stage 1'])-int(get_data["per_stages"]['all']['Stage 3'])
	flowchart_params_4 = get_data["per_stages"]['all']['Stage 3']
	flowchart_params_5 = int(get_data["per_stages"]['all']['Stage 3'])-int(get_data["per_stages"]['all']['Stage 5'])
	flowchart_params_6 = get_data["per_stages"]['all']['Stage 5']
	output = {}
	output['research']= get_data
	output['research']['per_author']['data']= get_data['per_author']['data'][0:9]
	output['research']['per_keyword']['data']= get_data['per_keyword']['data'][0:9]
	detail = {}
	if(get_file_url(id,'diagram_flowchart')):
		detail['diagram_flowchart'] = '<img src="'+get_file_url(id,'diagram_flowchart')+'" alt="Your Image">'
	detail['diagram_per_year_paper'] = '<img src="'+get_file_url(id,'diagram_per_year_paper')+'" alt="Your Image">'
	detail['diagram_per_year'] = '<img src="'+get_file_url(id,'diagram_per_year')+'" alt="Your Image">'
	detail['diagram_per_source'] = '<img src="'+get_file_url(id,'diagram_per_source')+'" alt="Your Image">'
	detail['diagram_per_author'] = '<img src="'+get_file_url(id,'diagram_per_author')+'" alt="Your Image">'
	detail['diagram_per_keyword'] = '<img src="'+get_file_url(id,'diagram_per_keyword')+'" alt="Your Image">'
	detail['diagram_sna_keyword'] = '<img src="'+get_file_url(id,'diagram_sna_keyword')+'" alt="Your Image">'
	
	##Research Query
	_table = """<table style="width: 80%; padding:5px; margin:10px">
                      <tr>
                        <th>Source</th>
                        <th>Keyword</th>
                      </tr>"""
	_whitespace = ''
	for _ in output['research']['result_keyword']:
		_temp = '<tr><td>'+str(_)+'</td><td>'+str(output['research']['result_keyword'][_])+'</tr>'
		_whitespace = _whitespace+_temp
	_table = _table+_whitespace+'</table>'
	detail['table_result_keyword'] = _table

	##table_per_stages
	_table = """<table style="padding:5px;margin:10px">
                <tr>
                  <th style="text-align: center;">Source</th>
                  <th style="text-align: center;">Identification</th>
                  <th style="text-align: center;">Eligibility</th>
                  <th style="text-align: center;">Screening</th>
                  <th style="text-align: center;">Included</th>
                </tr>"""
	_table_content = ''
	for _ in output['research']['per_stages']:
		_temp = '<tr>\
			<td>'+str(_)+'</td>\
			<td style="text-align: center;">'+str(output['research']['per_stages'][_]['Stage 1'])+'</td>\
			<td style="text-align: center;">'+str(output['research']['per_stages'][_]['Stage 3'])+'</td>\
			<td style="text-align: center;">'+str(output['research']['per_stages'][_]['Stage 4'])+'</td>\
			<td style="text-align: center;">'+str(output['research']['per_stages'][_]['Stage 5'])+'</td>\
			</tr>'
		_table_content = _table_content+_temp
	_all_table_content = _table+_table_content+'</table>'
	detail['table_per_stages'] = _all_table_content

	##table_per_year_paper
	_table = """<table style="padding:5px;  margin:10px"><tr><th>Source</th>"""
	_whitespace = ""
	for __ in output['research']['per_year']['year']:
		_temp = '<th>'+str(__)+'</th>'
		_whitespace = _whitespace+_temp
	_table = _table+_whitespace+'</tr><tr><td>Count</td>'
	_whitespace = ""
	for __ in output['research']['per_year']['data']['all']:
		_temp = '<td>'+str(output['research']['per_year']['data']['all'][__])+'</td>'
		_whitespace = _whitespace + _temp
	_table = _table+_whitespace+'</tr></table>'
	detail['table_per_year_paper'] = _table


	cur.execute('UPDATE research_slr SET details=%s WHERE id=%s',[json.dumps(detail),id])
	conn.commit()


    

def get_file_url(research_id,description):
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	try:
		cur.execute("select * from file_upload where research_id=%s AND description=%s",[research_id,description])
		related_papers = cur.fetchone()
		url = minio_client.presigned_get_object(bucket_name="asprof",object_name=related_papers[2],)
		return url
	except:
		return False

def update_file(fileupload,research_id,category,extension):
    conn = dbcon()
    path = upload_file(fileupload,extension)
    cur = conn.cursor(buffered=True)
    cur.execute("select * from file_upload where research_id=%s AND description=%s", [research_id, category])
    select_one = cur.fetchone()
    if(select_one):
        path_remove = select_one[2]
        minio_client.remove_object('asprof', path_remove)
        cur.execute('UPDATE file_upload SET path=%s WHERE research_id=%s AND description=%s',[path, research_id, category])
        conn.commit()
    else:
        cur.execute("INSERT INTO file_upload(research_id, path, description) VALUES(%s,%s,%s)",[research_id,path,category])
        conn.commit()
    
def upload_file(fileupload,extension):
	object_name = str(uuid.uuid4()) + extension
	path = 'web/'
	object_name = path+object_name
	try:
		minio_client.put_object("asprof", object_name, data=fileupload, length=fileupload.getbuffer().nbytes)
		return object_name
	except S3Error as e:
		return (f"Error uploading file: {e}") 

def diagram_per_year_paper(research_id):
    conn = dbcon()
    title = 'Systematic Literature Review'
    plt.clf()

	# conn.row_factory = sql.Ro
    cur = conn.cursor(buffered=True)
    cur.execute("select * from research_slr where id="+research_id)
    data = cur.fetchone()
    get_data = json.loads(data[11])
    all_data = get_data['per_year']
    barWidth = 0.3
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})
    # set height of bar
    IEEE = [all_data['data']["IEEE"][year] if year in all_data['data']["IEEE"] else 0 for year in all_data['year']]
    Sciencedirect = [all_data['data']["Sciencedirect"][year] if year in all_data['data']["Sciencedirect"] else 0 for year in all_data['year']]
    ACM = [all_data['data']["ACM Digital Library"][year] if year in all_data['data']["ACM Digital Library"] else 0 for year in all_data['year']]
    # Set position of bar on X axis
    br1 = np.arange(len(IEEE))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    ax.bar(br1, IEEE, color='orange', width=barWidth, edgecolor='grey', label='IEEE')
    ax.bar(br2, Sciencedirect, color='g', width=barWidth, edgecolor='grey', label='Sciencedirect')
    ax.bar(br3, ACM, color='b', width=barWidth, edgecolor='grey', label='ACM Digital Library')
    for i, v in enumerate(IEEE):
        ax.text(i - 0.1, v, str(v), color='black', fontweight='bold')
    for i, v in enumerate(Sciencedirect):
        ax.text(i + 0.15, v, str(v), color='black', fontweight='bold')
    for i, v in enumerate(ACM):
        ax.text(i + 0.4, v, str(v), color='black', fontweight='bold')

    ax.set_xlabel('Year', fontweight='bold', fontsize=15)
    # ax.set_ylabel('Students passed', fontweight='bold', fontsize=15)
    ax.set_xticks([r + barWidth for r in range(len(IEEE))])
    ax.set_xticklabels(all_data['year'])
    ax.legend()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer

def diagram_per_year(research_id):
    conn = dbcon()
    title = 'Systematic Literature Review'
    plt.clf()

	# conn.row_factory = sql.Ro
    cur = conn.cursor(buffered=True)
    cur.execute("select * from research_slr where id="+research_id)
    data = cur.fetchone()
    get_data = json.loads(data[11])
    all_data = get_data['per_year']
    
    data = all_data['data']['all']
    courses = list(data.keys())
    values = list(data.values())
    
    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(courses, values, color ='orange',width = 0.8)
    
    # add the total value in the center of each bar
    for i, v in enumerate(values):
        plt.text(i-0.1, v - 0.7, str(v), color='black', fontweight='bold', fontsize=20)

    
    plt.xlabel("Publish Year")
    plt.show()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer

def diagram_per_source(research_id):
    conn = dbcon()
    title = 'Systematic Literature Review'
    plt.clf()
	# conn.row_factory = sql.Ro
    cur = conn.cursor(buffered=True)
    cur.execute("select * from research_slr where id="+research_id)
    data = cur.fetchone()
    get_data = json.loads(data[11])
    publisher = get_data['per_publisher']
    del publisher['all']
    colors=['orange', 'green', 'blue']
    labels = list(publisher.keys())
    sizes = list(publisher.values())
    # Set default font size and style
    fig, ax = plt.subplots(figsize=(8, 6))    
    plt.rcParams.update({'font.size': 16, 'font.family': 'serif'})
    # Create pie chart with centered label text
    plt.pie(sizes, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%', textprops={'horizontalalignment':'center', 'verticalalignment':'center'})
    plt.axis('equal')
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    # upload_file(buffer,".png")
    return buffer

def diagram_per_author(research_id):
    conn = dbcon()
    title = 'Systematic Literature Review'
    plt.clf()
	# conn.row_factory = sql.Ro
    cur = conn.cursor(buffered=True)
    cur.execute("select * from research_slr where id="+research_id)
    data = cur.fetchone()
    get_data = json.loads(data[11])
    authors = get_data ['per_author']['data'][0:9]
    maths = [_[1] for _ in authors]
    index = [_[0] for _ in authors]
    df = pd.DataFrame({'maths': maths}, index=index)
    df = df.sort_values('maths', ascending=True)  # Sort the values in descending order
    fig, ax = plt.subplots(figsize=(8, 6))  # Set the figure size to 8x6 inches
    df.plot.barh(ax=ax, legend=False)
    ax.axhline(0, color='grey', linewidth=0.8)
    ax.bar_label(ax.containers[0])
    ax.set_yticklabels(list(reversed(index)))
    ax.tick_params(axis='y', which='major', labelsize=8)
    plt.tight_layout()  # Adjust the spacing between the plot elements
    plt.show()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    # upload_file(buffer,".png")
    return buffer

def diagram_per_keyword(research_id):
    conn = dbcon()
    title = 'Systematic Literature Review'
    plt.clf()
    cur = conn.cursor(buffered=True)
    cur.execute("select * from research_slr where id="+research_id)
    data = cur.fetchone()
    get_data = json.loads(data[11])
    authors = get_data ['per_keyword']['data'][0:9]
    maths = [_[1] for _ in authors]
    index = [_[0] for _ in authors]
    df = pd.DataFrame({'maths': maths}, index=index)
    df = df.sort_values('maths', ascending=True)  # Sort the values in descending order
    fig, ax = plt.subplots(figsize=(8, 6))  # Set the figure size to 8x6 inches
    df.plot.barh(ax=ax, legend=False)
    ax.axhline(0, color='grey', linewidth=0.8)
    ax.bar_label(ax.containers[0])
    ax.set_yticklabels(list(reversed(index)))
    ax.tick_params(axis='y', which='major', labelsize=8)
    plt.tight_layout()  # Adjust the spacing between the plot elements
    plt.show()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer


@app.route('/test-minio')
def test_minio():
    # Check if the server is running
    try:
        with open("this_text.txt", "rb") as file_data:
            file_stat = os.stat("this_text.txt")
            file_size = file_stat.st_size
            random_name = str(uuid.uuid4())
            file_name = random_name+".txt"
            bucket_name = "asprof"
            # Insert the file into the bucket
            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=file_name,
                data=file_data,
                length=file_size,
            )
    except S3Error as err:
        print(f"{bucket_name} bucket does not exist: {err}")



def literature_review_slr_result_crawling(research_id):
	# print("berhasil")
	output = {}
	conn = dbcon()
	cur = conn.cursor(buffered=True)
	id = research_id
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
		try:
			mykeyword = _[16].replace(" ,",",").replace(", ",",")
			split_keyword = mykeyword.split(",")
			for _mykeyword in split_keyword:
				all_category_data.append(unidecode(_mykeyword.lower()))
				# for __ in split_keyword:
				# 	if(all_category_data != __):
				# 		json_category_data = json_category_data + '{ from:"'+ all_category_data +'", to: "'+__+'"},'
		except:
			pass


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
		try:
			myauthor = _[4].replace(" ;",";").replace("; ",";")
			# print(myauthor)
			split_myauthor = myauthor.split(";")
			for _myauthor in split_myauthor:
				all_category_data_author.append(unidecode(_myauthor.lower()))
		except:
			pass
	# print("get author cat")
	per_author = {i:all_category_data_author.count(i) for i in all_category_data_author}	
	# print(per_author)
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
