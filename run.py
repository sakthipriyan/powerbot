'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

from powerbot.core import processor
from powerbot.database import access


def main():
    #access.create_database()
    #access.init_database()
    processor.main()
    
    
if __name__ == '__main__':
    main()