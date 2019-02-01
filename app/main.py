from flask import Flask, render_template
from flask_socketio import SocketIO
from eliza import analyze
import quote_mappers.quote_mapper as quote_mapper
import os
import sys

sys.path.append(os.getcwd())
from scrapers.scraper_images import get_image_location


# configs
eliza_messages = 1
database_size = 'medium'    

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
message_count = 0
message_list = ''
model = quote_mapper.loadGlove()

def main():
    socketio.run(app, debug=False)

@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, model=model, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
    if json['message'] != '':
        global message_list
        message_list += json['message'] + ' ' 
        global message_count
        message_count += 1
        flag = 0
        if message_count == 3:
            message_count = 0
            flag = 1
            eliza_ponders = {
                "user_name" : "Eliza",
                "message" : 'Hmmm ...'
              }
            socketio.emit('my response', eliza_ponders, callback=messageReceived)
            eliza_msg = quote_mapper.getQuote(message_list, model)
            message_list = ''
        else:
            eliza_msg = analyze(json['message'])

        eliza_says = {
            "user_name" : "Eliza",
            "message" : eliza_msg
          }
        socketio.emit('my response', eliza_says, callback=messageReceived)
        if  flag==1:
            flag = 0
            img_loc, img_name = get_image_location(eliza_msg,"withimages_wiseoldsayings.json")
            if img_loc != "" and img_name != "":
                img_msg = { 
                        "message" : img_loc+img_name
                        }                
                socketio.emit('image handler', img_msg, callback=messageReceived)
                img_loc = ""    
                img_name = ""

if __name__ == '__main__':
    main()
