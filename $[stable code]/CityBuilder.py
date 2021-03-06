from mxproxy import mx
import re
import time
import LoginManager



# 	___ 					   _	
#  / __)                  _   (_)                              
# | |__ _   _ ____   ____| |_  _  ___  ____   ___              
# |  __) | | |  _ \ / ___)  _)| |/ _ \|  _ \ /___)             
# | |  | |_| | | | ( (___| |__| | |_| | | | |___ |             
# |_|   \____|_| |_|\____)\___)_|\___/|_| |_(___/                                                               
# 


#------------------------------
def build(cityID,sid,bt,debug=0):
	"""
		arg:cityID> city id which the player wants get its building list. 
		arg:sid>	specific id of tile which needs to be upgraded.
		arg:bt>		type of building present on the sid
		var:postpayload> this object was seperately captured via browser requests
		return> None, since its a post function. and its output is junk
	"""
	postpayload={
	"__VIEWSTATE": "oyzb4H5sU2dLgDogNyBqS3zmA5AUeA1sze5fHIr5Oz5a5zTUBsSBtQ6Hf4jsPaeWuiEHUCWkRlo3RKm10YEV/fd/gf/syomjwyeFz3aRQz4=",
	"rcid": cityID,
	"__VIEWSTATEGENERATOR": "2465F31B",
	"__EVENTTARGET": f"ctl00$ctl00$body$content$building{bt}",
	"__EVENTARGUMENT": "build"
	}

	response=LoginManager.post(f'http://s1.mechhero.com/Building.aspx?sid={sid}&bt={bt}',postpayload,debug=debug)
	if response:
		print(f"BUILDER:INFO: order placed :: cityID={cityID},sid={sid},bt={bt} ")
	else:
		print(f'BUILDER:ERROR: failed order')

	time.sleep(1)


#------------------------------
def autobuild(cityID,btype,maxlvl=20,onlyidle=1,randmode=1):
	'''
		desc:
			select lowest building from each type and then place build order on them
		example:
			for example input 'bt' is a list [1,2,3] then crystal,gas,cells are polulated 
			and lowest building is placed order , total of 3 orders are placed in this case
		arg:cityID: 
			standard id argument of city
		arg:btype:
			building type which player wants to build, see the game's main docs for more info.
		kwarg:randmode:
			randomize build order? and remove any priorities,
		kwarg:maxlvl:
			max level the building can be placed order, target buildings higher than this level are ignored 
	'''
	LoginManager.save_city()
	buildTargets=[]
	allBuildings=get_buildings(cityID)
	if type(btype) is not list: #type conversion
		btype=[btype]
		# print("BUILDER: Please provide btype argument as list ~ [1,2,3]...")

	if randmode:
		btype=mx.shuffle(btype)

	if onlyidle: 
		b=[]
		for x in allBuildings:
			if 'building now' in x['title'] or 'queued' in x['title']:
				print('skipping',x)
				continue
			else:
				b.append(x)
		allBuildings=b


	for b in btype:
		try:
			filteredList=list(filter(lambda x:x['bt']==b, allBuildings))
			if filteredList:
				minBuilding=sorted(filteredList, key=lambda x:x['level'])[0]
				if minBuilding['level']>=maxlvl:
					print(f'skipping {minBuilding} , reason=maxlevel reached')
					continue
				buildTargets.append(minBuilding)


		except Exception as e:
			print(e)

	# print('btargets',buildTargets)
	[build(cityID,t['sid'],t['bt']) for t in buildTargets]
	return LoginManager.load_city()

#_________________________________________________
class Buildings:
	core= [0, 29, 30, 32, 41, 42]
	mines={'crystal':1,'gas':2,'cells':3}
	storages=[11,12,13,15]
	defense=[45,46,17]

#_________________________________________________
from Defaults import *
def city1_plan():
	'matured'

def city2_plan():
	autobuild(CITY2['cid'],btype=[45],maxlvl=20)

def city3_plan():
	autobuild(CITY3['cid'],btype=Buildings.core,maxlvl=10)
	# autobuild(CITY3['cid'],btype=[*range(100)],maxlvl=10)
	# autobuild(CITY3['cid'],btype=[3],maxlvl=10)
#_________________________________________________
def city4_plan():
	autobuild(CITY4['cid'],Buildings.mines['cells'],maxlvl=10)
	autobuild(CITY4['cid'],Buildings.core,maxlvl=10)#build these to lvl-1 first

def city5_plan():
	...




#_________________________________________________
#                 (_)                     | |     
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___ 
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
#-------------------------------------------------                                                              
if __name__ == '__main__':
	while True:
		autobuild(CITY6['cid'],[3,3,3],maxlvl=10)
		time.sleep(60)

	# print(get_resources(Defaults.CITY3))
