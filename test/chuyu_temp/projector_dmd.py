import pygame
import zmq
import os
import threading
import numpy as np



def process_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return False
    elif event.type == pygame.QUIT:
        return False
    return True

def array_to_surface(array):
    # Ensure the array is in the right format (8-bit per channel, 3 channels for RGB)
    if array.ndim == 2:  # Grayscale
        array = np.stack((array,) * 3, axis=-1)
    elif array.shape[2] == 1:  # Single channel, e.g., grayscale
        array = np.concatenate((array, array, array), axis=-1)

    # Convert the array to a Pygame surface
    surface = pygame.surfarray.make_surface(array.swapaxes(0, 1)/3)
    return surface





def display_loop(screen, screen_width, screen_height):
    global mode

    array = np.load('image_dmd.npy')
    # Convert the array to a Pygame surface
    surface = array_to_surface(array)

    while True:
        screen.blit(surface, (0, 0))
        pygame.display.flip()


def zmq_server(port):
    global mode

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    # socket.bind("ipc://zmq_viz")
    socket.bind("tcp://*:5555")
    print("server runs")
    #print(f"Server listening on port {port}. Waiting for movement signals...")

    while True:
        data = socket.recv_string()

        if data in [MOVE_LEFT, MOVE_RIGHT, DISPLAY_GRAY]:
            mode = data
            print("Received signal: "+mode)
            socket.send_string("ack")
        if data =='INIT':      
            print("Received signal: "+data)
            socket.send_string("ack INIT")
        if data =='off':      
            print("Received signal: "+data)
            socket.send_string("ack")
        else:
            print("Received signal: "+data)
        
        
def main():
    screen_width, screen_height = 1920, 1080

    x = screen_width
    y = 0
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
    # os.environ['SDL_VIDEO_FULLSCREEN_HEAD'] = "1"




    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height), flags = pygame.NOFRAME)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

 
    port = 8888

    zmq_thread = threading.Thread(target=zmq_server, args=(port,))
    zmq_thread.start()

    display_loop(screen, screen_width, screen_height)

    zmq_thread.join()
    
#     socket_thread = threading.Thread(target=socket_server, args=(port,))
#     socket_thread.start()

#     display_loop(screen, screen_width, screen_height, speed, stripe_width, gap_width)

#     socket_thread.join()
    pygame.quit()
    
    
if __name__ == '__main__':
    main()



