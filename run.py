'''
Created on 15-Dec-2012

@author: sakthipriyan
'''
from powerbot.database import access


def main():
    print 'hello'
    access.create_database()
    
if __name__ == '__main__':
    main()