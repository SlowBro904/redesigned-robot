""" Sets the version number variable based on the version number file """
from config import config
version = open(config['VERSION_NUMBER_FILE']).readlines().strip()