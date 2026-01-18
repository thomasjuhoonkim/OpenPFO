
from threading import Thread, Event
import pickle
import traceback
import sys
from time import sleep

#special code that is not generalizable
import openvsp_config
openvsp_config._IGNORE_IMPORTS = True
try:
    openvsp_config.LOAD_GRAPHICS = (sys.argv[2] == 'True')
except IndexError:
    pass
import openvsp as module

HOST = 'localhost'
try:
    PORT = int(sys.argv[1])
except IndexError:
    PORT = 0
event = Event()
global gui_wait
gui_wait = True
global gui_active
gui_active = False
debug = False

def pack_data(data, is_command_list=False):
    def sub_pack(sub_data):
        new_data = sub_data
        if isinstance(sub_data, module.vec3d):
            new_data = {"name":'vec3d',
                "x":sub_data.x(),
                "y":sub_data.y(),
                "z":sub_data.z(),
            }
        elif isinstance(sub_data, list) or isinstance(sub_data, tuple):
            if len(sub_data) > 0:
                if isinstance(sub_data[0], module.vec3d):
                    new_data = {
                        "name": "vec3d_list",
                        "list": []
                    }
                    for p in sub_data:
                        thing = {
                            "x":p.x(),
                            "y":p.y(),
                            "z":p.z(),
                        }
                        new_data['list'].append(thing)
                elif sub_data[0] == "error":
                    pass

        return new_data

    if is_command_list:

        #commands look like this: [func_name (str), args (list [arg1, arg2, argn]), kwargs (dict keyword1: arg1, kw2: arg2)  ]
        # example
        #                               [comp_name,     args,       dict]
        # vsp.compvecpnt01(uv_array) -> ["compvepnt01", [uv_array], {}  ]
        #
        new_data = [data[0], [], {}]
        for value in data[1]:
            new_data[1].append(sub_pack(value))
        for key, value in data[2].items():
            new_data[2][key] = sub_pack(value)
        new_data[1] = tuple(new_data[1])
    else:
       new_data = sub_pack(data)
    b_data = pickle.dumps(new_data)
    return b_data

def unpack_data(b_data, is_command_list=False):
    def sub_unpack(sub_data):
        n_data = sub_data
        if isinstance(sub_data, dict):
            if sub_data['name'] == 'vec3d':
                n_data = module.vec3d(sub_data['x'], sub_data['y'], sub_data['z'])
            elif sub_data['name'] == 'vec3d_list':
                n_data = []
                for r in sub_data['list']:
                    n_data.append(module.vec3d(r['x'], r['y'], r['z']))
        return n_data

    data = pickle.loads(b"".join(b_data))
    if is_command_list:
        new_data = [data[0], [], {}]
        for value in data[1]:
            new_data[1].append(sub_unpack(value))
        for key, value in data[2].items():
            new_data[2][key] = sub_unpack(value)
        new_data[1] = tuple(new_data[1])
    else:
       new_data = sub_unpack(data)

    return new_data

def start_server():
    import socket
    global gui_active
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server Socket Thread: Bound to {s.getsockname()}. Listening...", file=sys.stderr)
        conn, addr = s.accept()
        with conn:
            print("Server Socket Thread: Connected by %s, %s"%(addr[0], addr[1]))
            while True:
                b_data = []
                data = []
                # Wait for command
                while True:
                    try:
                        packet = conn.recv(1024)
                    except ConnectionResetError:
                        print("Socket ConnectionResetError")
                        break
                    if not packet: break
                    b_data.append(packet)
                    try:
                        data = unpack_data(b_data, is_command_list=True)
                        break
                    except (pickle.UnpicklingError, EOFError):
                        pass
                if b_data == [] or data == []:
                    print("Server Socket Thread: Unable to receive data from socket, closing server.")
                    break

                # Special functionality for StartGUI
                if data[0] == 'StartGUI':
                    if debug:
                        print("Server Socket Thread: StartGUI called")
                    if debug and event.is_set():
                        print("Server Socket Thread: The OpenVSP GUI should already be running")
                    result = 0
                    b_result = pack_data(result)
                    event.set()
                    if module.IsGUIBuild():
                        while not module.IsEventLoopRunning():
                            sleep(.01)

                # Special functionality for StopGUI
                elif data[0] == 'StopGUI':
                    if debug and not event.is_set():
                        print("Server Socket Thread: The OpenVSP GUI is not running")
                    if debug:
                        print("Server Socket Thread: About to call StopGUI()")
                    if module.IsEventLoopRunning():
                        module.StopGUI()
                    gui_active = False
                    if debug:
                        print("Server Socket Thread: After StopGUI() called")
                    result = 0
                    b_result = pack_data(result)

                # Special functionality for IsGUIRunning
                elif data[0] == 'IsGUIRunning':
                    result = gui_active
                    b_result = pack_data(result)

                # Regular functionality
                else:
                    func_name = data[0]
                    args = data[1]
                    kwargs = data[2]
                    foo = getattr(module, func_name)
                    try:
                        if debug:
                            print("Server Socket Thread: A1 Waiting for Lock")
                        if gui_active:
                            module.Lock()
                            if debug:
                                print("Server Socket Thread: A2 Lock obtained")
                        result = foo(*args, **kwargs)
                        if debug:
                            print("Server Socket Thread: A3 VSP function called")
                        if gui_active:
                            module.Unlock()
                            if debug:
                                print("Server Socket Thread: A4 Lock released")
                    except Exception as e:
                        exc_info = sys.exc_info()
                        result = ["error", ''.join(traceback.format_exception(*exc_info))]
                    b_result = pack_data(result)

                # Try to send response back
                try:
                    if debug:
                        print("Server Socket Thread: sending data back")
                    conn.sendall(b_result)
                except (ConnectionResetError, BrokenPipeError) as e:
                    print("Server Socket Thread: Unable to send data to socket, closing server.")
                    break

    print("Server Socket Thread: server closing")
    global gui_wait
    gui_wait = False
    event.set()
    module.StopGUI()
    print("Server Socket Thread: End of thread")


if __name__ == "__main__":
    t = Thread(target=start_server, args=())
    t.start()
    module.Lock()
    module.Unlock()
    while gui_wait:
        event.wait()
        if debug:
            print("Server GUI Thread: Starting GUI")
        if gui_wait: #makes sure this didnt change while waiting
            gui_active = True
            module.StartGUI()
        if debug:
            print("Server GUI Thread: GUI stopped")
        event.clear()
    print("Server GUI Thread: End of thread")

