from flask import Flask, request, make_response
from flask_restful import Resource, Api
import urllib3
import os
import json

http = urllib3.PoolManager()


app = Flask(__name__)
api = Api(app)

DETECTRON_URL = os.environ['DETECTRON_URL']
SCENEGRAPH_URL = os.environ['SCENEGRAPH_URL']
print(DETECTRON_URL, SCENEGRAPH_URL)

# print("define DETECTRON_URL and SCENEGRAPH_URL please")


class SgSrvc(Resource):
    def put(self, resource_path):
        img_url = request.form['data']
        res = http.request('PUT', DETECTRON_URL, fields={'url':img_url})
        print(res.data)
        cls_boxes = res.data
        if cls_boxes:
            sg_res = http.request('PUT', SCENEGRAPH_URL, fields={'url':img_url, 'data':cls_boxes})
            print(sg_res.data)
            sg_data = json.loads(sg_res.data)
            return sg_data
        else:
            return make_response("That url didn't work. Try another image url.")

api.add_resource(SgSrvc, '/<string:resource_path>')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5087)
