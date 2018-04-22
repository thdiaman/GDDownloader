import sys

class Logger:
	"""
	Class that implements a logger for the actions of this tool.
	"""
	def __init__(self, verbose, logto = sys.stdout):
		"""
		Initializes this logger. The verbose argument can be set to 0 for no messages,
		1 for simple messages, and 2 for progress bars.

		:param verbose: integer denoting the amount of output to be logged.
		:param logto: buffer where messages are logged.
		"""
		self.verbose = verbose
		self.logto = logto
		self.current_action_length = None
		self.current_action_step = 0
		self.last_print_action_step = 0

	def log_action(self, action):
		"""
		Logs an action.

		:param action: the message of the action to be logged.
		"""
		if self.verbose == 1 or self.verbose == 2:
			self.logto.write(action + "\n")

	def start_action(self, action, current_action_length = None):
		"""
		Logs the beginning of a multi-step action. See also methods step_action
		and end_action.

		:param action: the message of the action to be logged.
		:param current_action_length: the number of steps that an action consists of.
		"""
		self.current_action_length = current_action_length
		self.current_action_step = 0
		self.last_print_action_step = 0
		if self.verbose == 1 or self.verbose == 2:
			self.logto.write("\n" + action + "\n")

	def step_action(self):
		"""
		Signifies that a step of a multi-step action has been completed. See also
		methods start_action and end_action.
		"""
		self.current_action_step += 1
		if self.verbose == 2:
			fragment = self.current_action_step / self.current_action_length
			percentage = int(100 * fragment)
			progress_bar_size = 20
			progress_bar_fragment = int(fragment * progress_bar_size)
			whitespace = "  " if percentage < 10 else (" " if percentage < 100 else "")
			last_print_percentage = int(100 * self.last_print_action_step / self.current_action_length)
			if last_print_percentage != percentage:
				self.logto.write("\r[%s%s] %s%d%%" % ("-" * progress_bar_fragment, " " * (progress_bar_size - progress_bar_fragment), whitespace, percentage))
				self.last_print_action_step = self.current_action_step

	def end_action(self):
		"""
		Logs the end of an action (either single or multi-step).
		"""
		if self.verbose == 1:
			self.logto.write("Done!\n")
		elif self.verbose == 2:
			self.logto.write("\nDone!\n")
