import json
import queue
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import paginate


def main():
    app.run(debug=False, host='0.0.0.0', port=5001)


app = Flask(__name__)
CORS(app)


@app.route('/gallery/list', methods=['GET'])
def gallery_list():
    total = str(len(os.listdir(images_dir)))
    page_number = request.args.get('pageNumber')
    page_size = request.args.get('pageSize')
    if page_number is not None and page_size is not None:
        print("paginated, number: {}, size: {}".format(page_number, page_size))
        files = list(os.listdir(images_dir))
        files = paginate.Page(files, page=int(page_number), items_per_page=int(page_size)).items
        files = list([os.path.join('img', i) for i in files])
        return json.dumps({'items': files, 'total': total}), 200
    else:
        files = list([os.path.join('img', i) for i in os.listdir(images_dir)])
        return json.dumps({'items': files, 'total': total}), 200


if __name__ == '__main__':
    q = queue.Queue(0)
    # images_dir = 'D:\\projekty\\GTA-V-extractors\\output\\rgb-jpeg'
    images_dir = 'D:\\GTAV_extraction_output\\rgb-jpeg'
    main()
