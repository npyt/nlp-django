import json
import urllib.request
import requests
from tika import parser
from flask import Flask, make_response

apiURL = "http://localhost"
apiPort = "6570"

app = Flask(__name__)

def getFileContent(documentId):	
	response = requests.get(apiURL + ":" + apiPort + "/documents/" + documentId)	
	y = json.loads(response.content)
	documentURI = y["document_uri"]
	documentName = y["document_name"]
	
	urllib.request.urlretrieve(documentURI, "documents/" + documentName)
	parsedPDF = parser.from_file("documents/" + documentName)
	content= parsedPDF["content"]
	
	return content

@app.route('/documents/<documentId>/contents')
def index(documentId):
	response = make_response(getFileContent(documentId), 200)
	response.mimetype = "text/plain"
	return response
if __name__ == '__main__':
	app.run(debug=True)