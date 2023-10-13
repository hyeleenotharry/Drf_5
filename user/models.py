from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from book.models import Author


class UserManager(BaseUserManager):
    def create_user(self, email, username, nickname, birthday, profile, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not email:
            raise ValueError("Users must have email")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            nickname=nickname,
            birthday=birthday,
            profile=profile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, nickname, email, birthday, profile, password=None
    ):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            username=username,
            nickname=nickname,
            birthday=birthday,
            profile=profile
            # password=password,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=100)

    nickname = models.CharField(max_length=100)

    profile = models.ImageField(
        null=True,
        blank=True,
        upload_to="media/userProfile",
        default="media/userProfile/default.png",
    )

    birthday = models.DateField(blank=True, null=True)
    join_date = models.DateField(auto_now_add=True)

    follower = models.ManyToManyField(
        Author, symmetrical=False, related_name="followee", blank=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "nickname", "birthday", "profile"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
