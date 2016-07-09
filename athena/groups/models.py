from django.db import models
#from django.contrib.auth.models import User
# from users.models import UserProfile

class Group(models.Model):
	group_name = models.CharField(max_length=5000)
	create_date = models.DateTimeField('date created')
	creator_username = models.CharField(max_length=5000)#group creator (has power to delete group/etc)

	# uncomment me
	# group_members = models.ManyToManyField(UserProfile)	
	topic = models.CharField(max_length=500)
	
	OPEN = 'Open'
	CLOSED = 'Closed'
	SECRET = 'Secret'
	GROUP_CHOICES = (
		(OPEN, OPEN),
		(CLOSED, CLOSED),
		(SECRET, SECRET)
	)
	group_type = models.CharField(max_length=15,
				   choices = GROUP_CHOICES,
				   default=OPEN)

	# def get_all_users(self):
		
	def __str__(self):
		return self.group_name

# class GroupUserJoin(models.Model):
# 	user = models.ForeignKey(User, null=True)
# 	group = models.ForeignKey(Group)
