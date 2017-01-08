class Post:
	"""
	Class that defines Post Node
	"""
	def __init__(self, id, owner, text, reponses):
		self.id = id
		self.owner = owner
		self.text = text
		self.reponses = reponses


def classify_post(users):
	"""
	Function to classify whether a comment is a global poke, personal poke, friend poke or a combination of all
	Returns 
	0 - personal poke - nothing in users
	1 - global poke - global
	2 - friend poke - friend user name
	3 - global and friend poke - global and username specified
	4 - 
	"""
	if users == '' or users == ' ':
		return 0
	all_users = users.split(' ')
	global_flag = 0
	friend_flag = 0
	user_list = []
	for u in all_users:
		if u == 'global':
			global_flag = 1
		else:
			friend_flag = 1
			user_list.append(u)

	if global_flag == 1 and friend_flag == 1:
		return tuple((3, user_list))
	elif global_flag == 1:
		return 1
	elif friend_flag == 1:
		return tuple((2,user_list))


