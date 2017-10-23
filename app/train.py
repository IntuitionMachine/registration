
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.model import Metadata, Interpreter



builder = ComponentBuilder(use_cache=True)
training_data = load_data('/var/www/new/registration/data/examples/rasa/demo-rasa.json')

trainer = Trainer(RasaNLUConfig("/var/www/new/registration/sample_configs/config_spacy.json"),builder)
trainer.train(training_data)
model_directory = trainer.persist('/var/www/new/registration/projects/default/')
print ('dir')
print(model_directory)
config= RasaNLUConfig("/var/www/new/registration/sample_configs/config_spacy.json")
interpreter = Interpreter.load(model_directory,config,builder)




