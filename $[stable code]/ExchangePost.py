from __imports__ import *
DEBUG=0

def get_res_info(CITY):
	page=LoginManager.get_page_soup(f"http://s1.mechhero.com/City.aspx?cid={CITY['cid']}")
	ivals=re.search(r'(?<=initialize\().+(?=\))',str(page)).group().split(',')
	crystals=float(ivals[3])
	gas=float(ivals[6])
	cells=float(ivals[9])
	current=(crystals,gas,cells)
	capacity=(float(ivals[4]), float(ivals[7]) ,float(ivals[10]))

	deficit=[round(x,-3) for x in map(lambda x,y: x-y,capacity,current)]
	return {'current':current,'capacity':capacity,'deficit':deficit}

def get_transporters(CITY):
	u= LoginManager.get_page_soup(f'http://s1.mechhero.com/BuildingRouter.aspx?sid=35&bt=90&cid={CITY["cid"]}')
	u=u.select_one('.lpane > p:nth-child(3) > b:nth-child(2)').text
	transporter_count=int(re.search(r'\d*',u).group())
	return transporter_count

def make_transfer(FCITY,TCITY,resarray):
	resarray=*map(int,resarray),
	'http://s1.mechhero.com/Building.aspx?sid=35&bt=90'
	apiurl=f'http://s1.mechhero.com/Building.aspx?sid=35&bt=90&cid={FCITY["cid"]}'
	pd={
		"__VIEWSTATE": "qxtWJnc7zXieXG7kaEc35je+m512AZkn7dbGma/NUhvUwT2jQJih4NRgX0x6/OPUv4MKUfUuRQhfS7pr7MPI1mifPnMKEHffoyABgXgxQAQ=",
		"rcid": FCITY['cid'], "tid": 	(TCITY['cid']), "tcid": (FCITY['cid']),
		"res0": (resarray[0]), "res1": (resarray[1]), "res2": (resarray[2]),
		"tpid": "0",
		"tx": 	(TCITY['coords'][0]), "ty": 	(TCITY['coords'][1]),
		"tmv": "-1",
		"tspeed": "20",
		"__VIEWSTATEGENERATOR": "2465F31B", "__EVENTTARGET": "ctl00$ctl00$body$content$ctl01", "__EVENTARGUMENT": "transfer"
	}

	if DEBUG: print('TRANSFER:DEBUG:',pd)

	print(f"TRANSFER: F:{FCITY['cid']}->T:{TCITY['cid']} resources:{resarray}")
	return LoginManager.post(apiurl,pd)


def transfer_xsurplus(FROMCITY,TOCITY,balance=1,surplusdiv=2,xmin=30000,xbaseline=[100000,100000,75000],debug=0):
	'''
		will transfer the surplus production of SUPPLIER CITY to destination CITY
	'''
	sender=get_res_info(FROMCITY) ; receiver=get_res_info(TOCITY)
	surplus=[int(max(0,(a-b)/surplusdiv)) for a,b in zip(sender['current'],xbaseline)]
	sendable=[min(a,b) for a,b in zip(surplus,receiver['deficit'])]
	max_sendable=get_transporters(FROMCITY)*10000
	total_sendable=sum(sendable)

	if max_sendable<=total_sendable:
		scalefactor=max_sendable/total_sendable
		sendable=[int(n)for n in map(lambda x: x*scalefactor,sendable)]

	print(sendable)

	if sum(sendable)<=xmin:
		print(f"TRANSFER:FAIL: Min of [{xmin}] required for transferring ")
		return False

	# print(sender,sendable)
	if not debug:
		make_transfer(FROMCITY,TOCITY,sendable)
	return True


#________________________________________
#  __  __       ___ __    __  __  __  ___ 
# |  \|__)|\  /|__ |__)  /  `/  \|  \|__  
# |__/|  \| \/ |___|  \  \__,\__/|__/|___ 
#________________________________________
if 	__name__=='__main__':
	from __imports__ import *
	PRODUCERS=[CITY2,CITY5]
	CONSUMERS=[CITY6,CITY4]

	PRODUCER=PRODUCERS[0]



	
	# for CONSUMER in CONSUMERS:
	# 	(transfer_xsurplus(PRODUCER,CONSUMER))

	transfer_xsurplus(CITY2,CITY6,surplusdiv=2)





	# transfer_xsurplus(PRODUCERS[0],CITY1,resdiv=1)

