from flask import Flask, Response, request
import requests
import hashlib
import redis

app = Flask(__name__)
DEFAULT_NAME = 'Makito Bloggs'
SALT = "UNIQUE_SALT"
DNMONSTER_URL = 'http://dnmonster:8080/monster/'
CACHE = redis.StrictRedis(host='redis', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    name = DEFAULT_NAME
    if request.method == 'POST':
        name = request.form['name']

    salted_name = SALT + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    header = '<hmtl><head><title> Image from String</title></head><body>'
    body = '''<form method="POST">
              Hello <input type="text" name="name" value="{0}">
              <input type="submit" value="submit">
              </form>
              <p> That's how you look like:
              <img src="/image/{1}" />
              '''.format(name, name_hash)
    footer = '</body></html>'

    return header + body + footer


@app.route('/image/<name>')
def get_image(name):
    hit = CACHE.get(name)
    if hit:
        print('Hitting the image cache, baby!')
        return Response(hit, mimetype='image/png')

    url = DNMONSTER_URL + name + '?size=80'
    response = requests.get(url)
    image = response.content

    print("No image cache found, adding it to Redis...")
    CACHE.set(name, image)

    return Response(image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)
