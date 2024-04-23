import importlib.machinery
import importlib.util
import os
from utils import *

for mod in os.listdir(currentPath+"soundsRecognition"):
    if mod.endswith(".py"):
        loader = importlib.machinery.SourceFileLoader( mod, currentPath+"soundsRecognition/"+mod )
        spec = importlib.util.spec_from_loader( mod, loader )
        mymodule = importlib.util.module_from_spec( spec )
        loader.exec_module( mymodule )
        mymodule.test()