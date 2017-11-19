from rasa_core.actions.action import Action
from rasa_core.events import SlotSet

class ActionCreateAccount(Action):
	def name(self):
		return 'action_create_account'
	def run(self, dispatcher, tracker, domain):
		password=generate_random_password()
		user=tracker.get_slot('name')
		email=tracker.get_slot('email')
		dispatcher.utter_message("Thanks %user for subscribing! your username is %email and initial password is %password"%(user,email,password))
		return []