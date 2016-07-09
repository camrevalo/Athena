from django.db import models
from django.contrib.auth.models import User
from forum.models import Answer
from forum.models import Group

class UserProfile(models.Model):
    groups = models.ManyToManyField(Group)

	# Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Additional profile attributes
    picture = models.CharField(max_length=5000, default='Paste image URL here')

    school = models.CharField(max_length=500, default='school')
    isTeacher = models.BooleanField(default=False)
    firstName = models.CharField(max_length=500, default='first name')
    lastName = models.CharField(max_length=500, default='last name')
    upvotedAnswers = models.ManyToManyField(Answer, related_name='upvotedAnswers')
    downvotedAnswers = models.ManyToManyField(Answer, related_name='downvotedAnswers')

    def upvoted(self, answer):
        all_upvoted = self.upvotedAnswers.all()

        if answer in all_upvoted:
            return True
        else:
            return False

    def upvote(self, answer):
        self.upvotedAnswers.add(answer)
        self.save()

    def rm_upvote(self, answer):
        self.upvotedAnswers.remove(answer)
        self.save()

    def downvoted(self, answer):
        all_downvoted = self.downvotedAnswers.all()
        #print all_downvoted
        if answer in all_downvoted:
            return True
        else:
            return False

    def downvote(self, answer):
        self.downvotedAnswers.add(answer)
        self.save()

    def rm_downvote(self, answer):
        self.downvotedAnswers.remove(answer)
        self.save()

    def __unicode__(self):
        return self.user.username
