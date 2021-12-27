from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
	def create_user(self, email, fullname, password):
		if not email:
			raise ValueError('users must have Email')
		if not fullname:
			raise ValueError('users must have Fullname')

		user = self.model(email=self.normalize_email(email), full_name=fullname)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, fullname, password):
		user = self.create_user(email, fullname, password)
		user.is_admin = True
		user.is_seller = True
		user.save(using=self._db)
		return user