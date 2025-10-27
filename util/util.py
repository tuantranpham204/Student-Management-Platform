import os
from dotenv import load_dotenv
from types import SimpleNamespace as sn

load_dotenv()

default_vals = sn({
  "DEFAULT_BG_COLOR" : os.getenv("DEFAULT_BG_COLOR"),
})

attr = sn({

})