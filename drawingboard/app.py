# coding: utf-8

from . import create_app

def start():
    app = create_app({})
    app.run(debug=True,port=9090,host='0.0.0.0')

if __name__ == '__main__':
    start()