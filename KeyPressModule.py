import pygame


def init():
    # Initialize and create 100 x 100 window
    pygame.init()
    win = pygame.display.set_mode((100, 100))


def get_key(key_name):
    answer = False
    # Get all events
    for eve in pygame.event.get():
        pass
    # Get pressed key
    key_input = pygame.key.get_pressed()
    # Format key as K_value, with value being replaced with key_name
    my_key = getattr(pygame, 'K_{}'.format(key_name))
    # Determine if key_input has the desired value
    if key_input[my_key]:  # K_a = key_value
        answer = True
    pygame.display.update()
    return answer


def main():
    if get_key('LEFT'):
        print('Key left was pressed')
    if get_key('RIGHT'):
        print('Key right was pressed')


if __name__ == '__main__':
    init()
    while True:
        main()
