# You would think that doing
# from mreschke import fusionauth
# would allow you to use fusionauth.group.find()
# but it errors with "module 'mreschke.fusionauth' has no attribute 'group'"
# Although doing fusionauth.user.find() works, huh

# So import all the modules here
from . import app
from . import client
from . import group
from . import user
