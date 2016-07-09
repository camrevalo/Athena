from django.db import models
from groups.models import Group
from django.contrib.auth.models import User

class Question(models.Model):
	#question_text is also known as "title" of question
	question_text = models.CharField(max_length=500)
	body = models.TextField()
	pub_date = models.DateTimeField('date published')
	user = models.ForeignKey(User)
	#null groups in questions are questions that belong to global feed
	group = models.ForeignKey(Group, null=True, blank=True)
	
	#all possible subjects for a question. looking to be expanded in the future
	MATH = 'Math'
	PHYSICS = 'Physics'
	CHEMISTRY = 'Chemistry'
	BIOLOGY = 'Biology'
	SUBJECT_CHOICES = (
		(MATH, MATH),
		(PHYSICS, PHYSICS),
		(CHEMISTRY, CHEMISTRY),
		(BIOLOGY, BIOLOGY),
	)
	
	subject = models.CharField(max_length=15,
				   choices = SUBJECT_CHOICES,
				   default=MATH)

	# the following methods are used by forum ranking mechanism (sort by teachers, sort by upvote)
	def answers_by_vote(self):
		return self.answer_set.order_by('-upvotes')

	def teacher_answers(self):
		users = User.objects.exclude(is_staff = "True")
		teachers = []
		for user in users:
			if user.userprofile.isTeacher:
				teachers.append(user)
		
		t_answers = self.answer_set.filter(user__in = teachers)
		return t_answers.order_by('-upvotes')

	def student_answers(self):
		users = User.objects.exclude(is_staff = "True")
		students = []
		for user in users:
			if not user.userprofile.isTeacher:
				students.append(user)
		
		s_answers = self.answer_set.filter(user__in = students)
		return s_answers.order_by('-upvotes')

	def top_teacher_answers(self):
		answers = self.teacher_answers()
		if len(answers) > 2:
			return answers[:2]
		else:
			return answers

	def top_student_answers(self):
		answers = self.student_answers()
		if len(answers) > 5:
			return answers[:5]
		else:
			return answers

	def num_student_answers(self):
		return len(self.student_answers())

	def num_teacher_answers(self):
		return len(self.teacher_answers())
	
	#function used for debugging purposes
	def __str__(self):
		return self.question_text + str(self.pub_date)

class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer_text = models.TextField()
	user = models.ForeignKey(User)
	upvotes = models.IntegerField(default=0)

	#upvotes first check if user has already upvoted on this kind of question
	def upvote(self, voter_id):
		user = User.objects.get(id = voter_id)
		has_upvoted = user.userprofile.upvoted(self)
		has_downvoted = user.userprofile.downvoted(self)
		color_arrow = True
		#if has downvoted, could undo downvote
		if not has_upvoted and not has_downvoted:
			user.userprofile.upvote(self)
			print "\n\nnot voted\n\n"
			self.upvotes = self.upvotes + 1
		elif not has_upvoted and has_downvoted:
			user.userprofile.rm_downvote(self)
			user.userprofile.upvote(self)
			print "\n\ndown voted but not up\n\n"
			self.upvotes = self.upvotes + 2
		else:
			user.userprofile.rm_upvote(self)
			self.upvotes = self.upvotes - 1
			color_arrow = False
			print "\n\nalready up voted\n\n"

		self.save()
		return color_arrow

	def downvote(self, voter_id):
		user = User.objects.get(id = voter_id)
		has_upvoted = user.userprofile.upvoted(self)
		has_downvoted = user.userprofile.downvoted(self)
		color_arrow = True
		if not has_downvoted and not has_upvoted:
			user.userprofile.downvote(self)
			print "\n\nnot voted\n\n"
			self.upvotes = self.upvotes - 1
		elif not has_downvoted and has_upvoted:
			user.userprofile.rm_upvote(self)
			user.userprofile.downvote(self)
			print "\n\up voted but not down\n\n"
			self.upvotes = self.upvotes - 2
		else:
			user.userprofile.rm_downvote(self)
			self.upvotes = self.upvotes + 1
			color_arrow = False
			print "\n\nalready down voted\n\n"

		self.save()
		return color_arrow


	def __str__(self):
		return self.answer_text
