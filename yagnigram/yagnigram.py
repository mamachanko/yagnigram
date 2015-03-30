"""
Usage:
    yagnigram feed [--count=<count>] [--no-images] [--use-cache] [--token=<token>] [--tokenfile=<tokenfile>] [--interactive] [--width=<width>] [--animate]
    yagnigram show <id>
    yagnigram oauth [--force] [--outputfile=<outputfile>]
    yagnigram flush_cache
    yagnigram --help
    yagnigram --version

Options:
    --help                     shows this screen
    --version                  shows version
    --count=<count>            how many media to show [default: 1]
    --width=<width>            image width [default: 100]
    --no-images                does not download and render images
    --use-cache                uses local image cache
    --token=<token>            Instagram access token
    --tokenfile=<tokenfile>    file containing the Instagram access token [default: ~/.yagnigram]
    --interactive              use interactive mode
    --animate                  animates videos
    --force                    overwrites the existing token
    --outputfile=<outputfile>  the file to write the token to [default: ~/.yagnigram]

"""
import sys
import os

import blessings
from docopt import docopt

from oauth import handle_oauth
from feed import Feed


class Yagnigram(object):

    def __init__(self, argv):
        self.argv = argv

    @classmethod
    def main(cls, argv=None):
        cls(argv).run()

    def run(self):
        self.arguments = docopt(doc=__doc__, argv=self.argv, version='yagnigram 0.1.0')
        self.terminal = blessings.Terminal()
        print('Welcome to ' + self.terminal.bold('yagnigram') + '\n--')

        if self.arguments['oauth']:
            self.on_oauth()

        if self.arguments['feed']:
            self.on_feed()

        print('--\nbye')

    def on_oauth(self):
        output_file = os.path.expanduser(self.arguments['--outputfile'])
        if self.arguments['--force']:
            try:
                os.remove(output_file)
            except OSError:
                pass
        raw_input('press any key to continue in the browser\n')
        handle_oauth(output_file=output_file)
        print('\nYour Instagram access token has been written to  %s.' % output_file)
        print('Thank you.')

    def on_feed(self):
        if self.arguments['--token']:
            token = self.arguments['--token']
        else:
            token_file = os.path.expanduser(self.arguments['--tokenfile'])
            with open(token_file, 'r') as f:
                token = f.readline()
        width = int(self.arguments['--width'])
        count = int(self.arguments['--count'])

        if self.arguments['--interactive']:
            try:
                for feed_item in Feed(token, count=count):
                    with self.terminal.fullscreen():
                        
                        with self.terminal.location(0, 0):
                            width = min(self.terminal.width, self.terminal.height*2)*2
                            print(feed_item.render(width))

                        with self.terminal.location(0, self.terminal.height-1):
                            raw_input('next (enter)')
            except KeyboardInterrupt:
                pass

        else:
            for feed_item in Feed(token, count=count):
                print(feed_item.render(width))


if __name__ == '__main__':
    Yagnigram.main(sys.argv[1:])
