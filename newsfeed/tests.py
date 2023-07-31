from django.test import TestCase
from django.contrib.auth.models import User
from .models import Newsfeed, Tags, UserInfo


class NewsfeedModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        tags1 = Tags.objects.create(name='tag1', owner=user)
        tags2 = Tags.objects.create(name='tag2', owner=user)
        newsfeed = Newsfeed.objects.create(
            photos='photo1.jpg',
            description='Test description',
            user_id=user
        )
        newsfeed.tags.add(tags1, tags2)

    def test_str_method(self):
        newsfeed = Newsfeed.objects.get(id=1)
        expected_str = f"{newsfeed.user_id}'s photos"
        self.assertEqual(str(newsfeed), expected_str)

    def test_photos_field(self):
        newsfeed = Newsfeed.objects.get(id=1)
        photos = newsfeed.photos
        self.assertEqual(photos, 'photo1.jpg')

    def test_description_field(self):
        newsfeed = Newsfeed.objects.get(id=1)
        description = newsfeed.description
        self.assertEqual(description, 'Test description')

    def test_user_id_field(self):
        newsfeed = Newsfeed.objects.get(id=1)
        user_id = newsfeed.user_id
        self.assertEqual(user_id.username, 'testuser')

    def test_likes_field(self):
        newsfeed = Newsfeed.objects.get(id=1)
        likes = newsfeed.likes.all()
        self.assertEqual(len(likes), 0)

    def test_tags_field(self):
        newsfeed = Newsfeed.objects.get(id=1)
        tags = newsfeed.tags.all()
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0].name, 'tag1')
        self.assertEqual(tags[1].name, 'tag2')


class UserInfoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        UserInfo.objects.create(id=user, profile_photo='photo.jpg', biography='Test biography')

    def test_str_method(self):
        userinfo = UserInfo.objects.get(id=1)
        expected_str = f"Info about testuser"
        self.assertEqual(str(userinfo), expected_str)

    def test_profile_photo_field(self):
        userinfo = UserInfo.objects.get(id=1)
        profile_photo = userinfo.profile_photo
        self.assertEqual(profile_photo, 'photo.jpg')

    def test_biography_field(self):
        userinfo = UserInfo.objects.get(id=1)
        biography = userinfo.biography
        self.assertEqual(biography, 'Test biography')


class TagsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        Tags.objects.create(name='tag1', owner=user)

    def test_str_method(self):
        tag = Tags.objects.get(id=1)
        expected_str = f'tag1 [{tag.owner}]'
        self.assertEqual(str(tag), expected_str)

    def test_name_field(self):
        tag = Tags.objects.get(id=1)
        name = tag.name
        self.assertEqual(name, 'tag1')

    def test_owner_field(self):
        tag = Tags.objects.get(id=1)
        owner = tag.owner
        self.assertEqual(owner.username, 'testuser')
