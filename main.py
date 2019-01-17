from flask import Flask, render_template
from flask_socketio import SocketIO
from eliza import analyze
import quote_mappers.quote_mapper as quote_mapper

app = Flask(__name__)
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
        print(message_count)
        if message_count == 3:
            message_count = 0
            eliza_msg = quote_mapper.getQuoteForInput(message_list, model)
        else:
            eliza_msg = analyze(json['message'])

        eliza_says = {
            "user_name" : "Eliza",
            "message" : eliza_msg
          }
        socketio.emit('my response', eliza_says, callback=messageReceived)

if __name__ == '__main__':
    main()
