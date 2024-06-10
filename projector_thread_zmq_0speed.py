import pygame
import zmq
import os
import threading
import numpy as np

MOVE_LEFT = "omrl"
MOVE_RIGHT = "omrr"
DISPLAY_GRAY = "gray50"

mode = MOVE_LEFT

def process_event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return False
    elif event.type == pygame.QUIT:
        return False
    return True

def display_loop(screen, screen_width, screen_height, speed, stripe_width, gap_width):
    global mode
    offset = 0

    while True:
        for event in pygame.event.get():
            if not process_event(event):
                return

        if mode == DISPLAY_GRAY:
            screen.fill((128, 128, 128))
        else:
            offset += speed if mode == MOVE_RIGHT else -speed
            draw_moving_stripes(screen, screen_width, screen_height, offset, stripe_width, gap_width)

        pygame.display.flip()

def draw_moving_stripes(screen, screen_width, screen_height, offset, stripe_width, gap_width):
    screen.fill((100, 100, 100))
    stripe_color = (0, 0, 0)
    total_width = stripe_width + gap_width

    for x in range(int(offset % total_width - total_width) + int(np.floor(screen_width/8)), int(np.floor(7*screen_width/8)), total_width):
        pygame.draw.rect(screen, stripe_color, (x, 1*screen_height/8, stripe_width, 5*screen_height/8))

# def socket_server(port):
#     global mode

#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(('', port))
#     server_socket.listen(1)

#     #print(f"Server listening on port {port}. Waiting for movement signals...")

#     while True:
#         client_socket, addr = server_socket.accept()
#         #print(f"Connection from {addr} established.")

#         data = client_socket.recv(1024).decode('utf-8')

#         if data in [MOVE_LEFT, MOVE_RIGHT, DISPLAY_GRAY]:
#             mode = data
#             #print(f"Received signal: {mode}")

#         client_socket.close()

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
    pygame.init()
    x = 0
    y = 0
    os.environ['SDL_VIDEO_FULLSCREEN_DISPLAY'] = f"{x},{y}"
    os.environ['SDL_VIDEO_FULLSCREEN_HEAD'] = "1"

    # screen = pygame.display.set_mode((screen_width, screen_height))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Moving Stripes')

    speed = 0
    stripe_width = 10
    gap_width = 10

    port = 8888

    zmq_thread = threading.Thread(target=zmq_server, args=(port,))
    zmq_thread.start()

    display_loop(screen, screen_width, screen_height, speed, stripe_width, gap_width)

    zmq_thread.join()
    
#     socket_thread = threading.Thread(target=socket_server, args=(port,))
#     socket_thread.start()

#     display_loop(screen, screen_width, screen_height, speed, stripe_width, gap_width)

#     socket_thread.join()
    pygame.quit()
    
    
if __name__ == '__main__':
    main()



