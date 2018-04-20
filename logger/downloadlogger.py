import sys

class Logger:
	def __init__(self, verbose, logto=sys.stdout):
		self.verbose = verbose
		self.logto = logto
		self.current_action_length = None
		self.current_action_step = 0
		self.last_print_action_step = 0

	def log_action(self, action):
		if self.verbose == 1 or self.verbose == 2:
			self.logto.write(action + "\n")

	def start_action(self, action, current_action_length=None):
		self.current_action_length = current_action_length
		self.current_action_step = 0
		self.last_print_action_step = 0
		if self.verbose == 1 or self.verbose == 2:
			self.logto.write("\n" + action + "\n")

	def step_action(self):
		self.current_action_step += 1
		if self.verbose == 2:
			fragment = self.current_action_step / self.current_action_length
			percentage = int(100 * fragment)
			progress_bar_size = 20
			progress_bar_fragment = int(fragment * progress_bar_size)
			whitespace = "  " if percentage < 10 else (" " if percentage < 100 else "")
			last_print_percentage = int(100 * self.last_print_action_step / self.current_action_length)
			if last_print_percentage != percentage:
				self.logto.write("\r[%s%s] %s%d%%" %("-" * progress_bar_fragment, " " * (progress_bar_size - progress_bar_fragment), whitespace, percentage))
				self.last_print_action_step = self.current_action_step

	def end_action(self):
		if self.verbose == 1:
			self.logto.write("Done!\n")
		elif self.verbose == 2:
			self.logto.write("\nDone!\n")
