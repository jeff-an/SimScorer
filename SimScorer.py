from flask import Flask
from flask import request, jsonify
from scorer import computeScore

app = Flask(__name__)

@app.route('/score', methods=['POST'])
def score():
  content = request.get_json(force = True)
  print("Received data: ", content)

  usertitle = content['title']
  comparingTitle = len(usertitle) > 4
  userdescription = content['description']
  for record in content['candidates']:
    if comparingTitle:
      # Compute name similarity and description similarity
      namescore = computeScore(usertitle, record['title'])
      ideascore = computeScore(userdescription, record['tagline'])
      record['namescore'] = namescore
      record['ideascore'] = ideascore
    else:
      ideascore = computeScore(userdescription, record['tagline'])
      record['ideascore'] = ideascore
  results = {}
  content['candidates'].sort(key=lambda x: x['ideascore'], reverse=True)
  results['idea'] = content['candidates'][:4]
  if comparingTitle:
    content['candidates'].sort(key=lambda x: x['namescore'], reverse=True)
    results['name'] = content['candidates'][:4]
  return jsonify(results)


if __name__ == '__main__':
  app.run()
