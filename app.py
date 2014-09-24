# coding: utf-8

from drawingboard import create_app

def start():
    app = create_app({})
    app.run(debug=True,port=9090)

if __name__ == '__main__':
    start()