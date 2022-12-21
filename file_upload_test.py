from deta import Deta
from dotenv import load_dotenv 
import os

try:
    load_dotenv(".db_env")
except:
    pass
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)

# create and use as many Drives as you want!
photos = deta.Drive("userdata")
photos.put("leonardoferrisi.json", path="./leonardoferrisi.json")