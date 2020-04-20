"""
Author: Jay
IPC
"""
import socketio
import eventlet
import sys
import logger as lg
import func as fx

# usage
def usage():
    print('Usage: python {} <interface>'.format(sys.argv[0]))
    sys.exit(1)

## socket defaults
sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': '../index.html'}
})

# events
@sio.on('connect')
def connect(sid, environ):
    lg.success('Client socket opened => {}'.format(sid))

@sio.on('disconnect')
def disconnect(sid):
    lg.error('Client socket closed => {}'.format(sid))


# daemon
if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()

    eventlet.wsgi.server(eventlet.listen((fx.network_config['host'], fx.network_config['port'])), app)
