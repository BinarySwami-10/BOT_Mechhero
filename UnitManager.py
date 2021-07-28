import Defaults
import LoginManager
import time

from multiprocessing.pool import ThreadPool
POOL=ThreadPool(8)
# from threading import Thread

def get_unit_data(UID):
	apiurl=f'http://s1.mechhero.com/data.dt?provider=unit&uid={UID}'
	data=LoginManager.get_page_soup(apiurl)
	name=data.select_one('.name').text
	status=data.select_one('.status').text
	isFree=True if 'Standing-by' in status else False
	dmgPerSecond=sum(int(x.text) for x in data.select('.damage b'))
	cellUsage=int(data.select_one('.res').text)
	# print('uid:',UID,end='|')
	return {'uid':UID,'name':name,'isFree':isFree,'dps':dmgPerSecond,'cells':cellUsage}

def get_units_list(CITY):
	geturl=f'http://s1.mechhero.com/UnitList.aspx?cid={CITY["cid"]}'
	unitlist=[x.attrs['data-uid'] for x in LoginManager.get_page_soup(geturl).select('.ubox')]
	return unitlist

def get_unit_datalist(CITY):
	# global ThreadPool
	return [y.get() for y in [POOL.apply_async(get_unit_data,(x,)) for x in get_units_list(CITY)]]

def rearm_repair_all_units(CITY,debug=0):
	postdata={
		"__VIEWSTATE": "IzwrWd9rYlF+vy4xX1zSXXuu/+4K6em0a7LKgZd70R9WxsLYAjNHSYgekv22BZ2tu5Lmh3FwCmrndZIJ4lWiOIUEJfSUQKyZFXFczbeCOEA=",
		"rcid": CITY['cid'],
		"__VIEWSTATEGENERATOR": "410BFDDA",
		"__EVENTTARGET": "ctl00$ctl00$body$content$unitControl",
		"__EVENTARGUMENT": "rearm_7"
	}
	uniturls=[f'http://s1.mechhero.com/Unit.aspx?uid={uid}' for uid in get_units_list(CITY)]
	futures=[]
	for x in uniturls:
		futures.append (POOL.apply_async(LoginManager.post,(x,postdata) ))
		if debug: 
			print(f'LOG: {__name__}:orderedrearm+repair->',x)
		time.sleep(1)

	wait=[r.wait() for r in futures]
	print('Ordered Rearm+Repair to All units in ',CITY['cid'])


if __name__ == '__main__':
	'''GET ALL UNITS'''
	# ulist=get_units_list(Defaults.CITY1)

	'''GET ALL DATA'''
	udata=get_unit_data(80725)
	print(udata)

	'''AUTO MAINTAIN ALL UNITS'''
	# rearm_repair_all_units(Defaults.CITY1)
