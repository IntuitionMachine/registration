
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.model import Metadata, Interpreter



builder = ComponentBuilder(use_cache=True)
#training_data = load_data('/var/www/new/registration/data/examples/rasa/demo-rasa.json')
training_data = load_data('data/examples/rasa/demo-rasa.json')
trainer = Trainer(RasaNLUConfig("sample_configs/config_defaults.json"),builder)
#trainer = Trainer(RasaNLUConfig("/var/www/new/registration/sample_configs/config_defaults.json"),builder)
#trainer = Trainer(RasaNLUConfig("sample_configs/config_spacy.json"),builder)

trainer.train(training_data)
#model_directory = trainer.persist('/new/registration/projects/default/')
model_directory = trainer.persist('projects/default/')
print ('dir')
print(model_directory)
config= RasaNLUConfig("sample_configs/config_defaults.json")
#config= RasaNLUConfig("/var/www/new/registration/sample_configs/config_defaults.json")
print('config')
print(config)
#config = RasaNLUConfig("sample_configs/config_spacy.json")
interpreter = Interpreter.load(model_directory,config,builder)

print (interpreter.parse(u'hello there mate,I am Carlos Perez.'))
print( interpreter.parse(u'They call me ed'))
print (interpreter.parse(u'dealexander@dot.state.az.us is my email'))
#print (interpreter.parse(u'Hello there mate,dealexander@dot.state.az.us is my email'))


