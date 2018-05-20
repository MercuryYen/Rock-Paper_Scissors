import telegram

#out = 1,2,3(Rock,Paper,Scissors)

class game(object):
	"""docstring for ClassName"""
	
	
	def __init__(self, identity):
		super(game, self).__init__()
		self.identity = identity
		self.players = list()
		self.out = list()
	def new(self,identity):
		
		return
	def join(self,User):
			if not User in self.players:
				self.players.append(User)
				self.out.append(0)
				return User.first_name + " "+User.last_name+"加入賽局"
			else:
				return "已經加入了"

		
		