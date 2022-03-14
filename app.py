from turtle import delay
from flask import Flask, send_from_directory, Response
import socket
import os, time
from datetime import datetime

serv = 0
addr = ("", 3000)  # all interfaces, port 8080
app = Flask(__name__)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_my_message(msg, __method = 1):
    global serv
    msg = bytes(msg.encode('utf-8'))
    print("method called")
    if serv != 1:
        if __method == None:
            s.bind(addr)
        else:
            s = socket.create_server(addr)
        serv = 1

    s.sendall(msg)
    s.send(msg)
    data = s.recv(1024)
    print(data)
    s.close()


react_folder = 'streaming-tutorial'
directory= os.getcwd()+ f'/{react_folder}/build/static'


@app.route('/')
def index():
    ''' User will call with with thier id to store the symbol as registered'''
    path= os.getcwd()+ f'/{react_folder}/build'
    print(path)
    return send_from_directory(directory=path,path='index.html')

#
@app.route('/static/<folder>/<file>')
def css(folder,file):
    ''' User will call with with thier id to store the symbol as registered'''
    
    path = folder+'/'+file
        
    return send_from_directory(directory=directory,path=path)

@app.route('/stream')
def stream():

    def get_data():

        while True:
            #gotcha
            time.sleep(1)
            
            msg = "Hello World TEST"
            # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #     s.bind(('0.0.0.0', 3050))
            send_my_message(msg)
            yield f'data: {datetime.now().second} \n\n'

    return Response(get_data(), mimetype='text/event-stream')

if __name__ == '__main__':
    resp = app.run(debug=True)