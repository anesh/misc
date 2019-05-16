import configparser
config = configparser.RawConfigParser()


out=config.read('master_inventory.ini')
print out
