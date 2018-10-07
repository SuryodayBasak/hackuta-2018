from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from algoliasearch import algoliasearch 
import simplejson as json
import time
import datetime
from os import walk

mypath = '/home/suryo/Desktop/HackUTA_py/Image_in'

app = ClarifaiApp(api_key = 'bf4cee40f7e44e4dbae18e26a2f803f4')

client = algoliasearch.Client("UBDU7AZZQQ", '67b1a31a36134503a27c597116b329bb')
index = client.init_index('project1')
index = client.init_index("newec")

filename = None
done_img = []
printf_line = []
printo_line = []
count = 0

while 1:
	now_img = []
	for (dirpath, dirnames, filenames) in walk(mypath):
		now_img.extend(filenames)
	print("\nCurrent images in the directory:\n",now_img,"\n\n")
	


	for after in now_img:
		if after not in done_img:
			filename = after
			break
		else:
			filename = None

	print("\n\nFilename:",filename,"\n") 		
    
	if filename:
		url = mypath+"/"+filename
		
		print("\nCurrent file name:",filename)		

		model = app.models.get('general-v1.3')
		image = ClImage(file_obj=open(url,'rb'))
		result = model.predict([image])
		
		print("\n\nClarifai API returns:\n",result,"\n\n")	
		
		data = result['outputs'][0]['data']['concepts']
		pred_list = []
		for comp in data:
			pred_list.append(comp['name'])
		
		(date,hmm) = result['outputs'][0]['created_at'].split('T')
		
		now =datetime.datetime.now().time()
		now.isoformat()

		batch = json.load(open("/home/suryo/Desktop/HackUTA_py/newec.json"))
		index.add_objects(batch)
		index.set_settings({"searchableAttributes": ["category", "type"]})

		ex = []
		final_op = {}
		for keyword in pred_list:
			temp = index.search(keyword)['hits']
			if temp:
				ex.append(temp[0])
		
		print("\n\nAlgolia API return:\n",ex,"\n\n")		
		
		for (num,ele) in enumerate(ex,start = 0):
			if num == 0:
				final_op=ele
			elif ex[num]['category'] != ex[num-1]['category']:
				final_op=ele
			
		out = {}
		for key,value in final_op.items():
			if (key == 'category') or (key == 'city') or (key =='state'):
				out[key] = value
		out['date'] = date
		out['time'] = now.isoformat()

		if out['category'] == "Fire":
			with open('firedpt.json','w') as of:
				of.write("data = \'")
				printf_line.append(out)				
				json.dump(printf_line,of)
				of.write("\';")
				of.write('\n')
			with open('policedpt.json','w') as of:
				of.write("data = \'")
				printo_line.append(out)
				json.dump(printo_line,of)
				of.write("\';")
				of.write('\n')
			with open('insurence.json','w') as of:
				of.write("data = \'")
				json.dump(printo_line,of)
				of.write("\';")
				of.write('\n')
			done_img.append(filename)
			print("\nUpdated files for Fire Damage")
		
		else:
			with open('policedpt.json','w') as of:
				of.write("data = \'")
				printo_line.append(out)
				json.dump(printo_line,of)
				of.write("\';")
				of.write('\n')
			with open('insurence.json','w') as of:
				of.write("data = \'")
				json.dump(printo_line,of)
				of.write("\';")
				of.write('\n')
			done_img.append(filename)
			print("\nUpdated files for Automobile damage/Vandalism")
	
	print("\n\nDone images:",done_img,"\n")	
	
	count+=1
	print("\n Loop ",count)
	time.sleep(15)		