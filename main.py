from cast import VideoPlayer
from time import sleep

if __name__ == '__main__':
    player = VideoPlayer()
    player.add('https://www.youtube.com/watch?v=oPpzJAzdpTU')
    # player.add('https://www.youtube.com/watch?v=TMnStKVzMGk')

    player.play()
    # player.pause()
    # sleep(1)
    # player.next()
    player.seek(0.65)
    # sleep(35)
    # player.next()

    player.main()
