import json
import urllib.request
import requests
from tika import parser
from flask import Flask, make_response

apiURL = "http://localhost"
apiPort = "6570"

app = Flask(__name__)

def getToken():
	headers = {'Content-Type': 'application/json'}
	data = {'credential': 'userAdmin', 'password':'utn.frba.nlp'}
	r = requests.post(apiURL + ":" + apiPort + "/api/auth/signin", data=json.dumps(data), headers=headers)
	
	return json.loads(r.text)["access_token"]

def getFileContent(documentId):
	token = getToken();
	
	headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
	print(headers)
	response = requests.get(apiURL + ":" + apiPort + "/documents/" + documentId, headers=headers)
	
	y = json.loads(response.content)
	documentURI = y["document_uri"]
	documentName = y["document_name"]	
	
	opener = urllib.request.build_opener()
	opener.addheaders = [('Authorization', 'Bearer ' + token)]
	urllib.request.install_opener(opener)

	urllib.request.urlretrieve(documentURI, "documents/" + documentName)
	parsedPDF = parser.from_file("documents/" + documentName)
	content= parsedPDF["content"]
	
	return content

@app.route('/documents/<documentId>/contents')
def index(documentId):
	response = make_response(getFileContent(documentId), 200)
	response.mimetype = "text/plain"
	return response

app.run(host='0.0.0.0', port=4242)