# from django.test import TestCase
# from django.contrib.auth.models import User
# from ..models import Tags, Photo, Newsfeed, UserInfo


# class NewsfeedModelTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='testuser', password='testpassword')

#         cls.tag1 = Tags.objects.create(name='Tag1')
#         cls.tag2 = Tags.objects.create(name='Tag2')

#         cls.photo1 = Photo.objects.create(photo='newsfeed_photos/photo1.jpg')
#         cls.photo2 = Photo.objects.create(photo='newsfeed_photos/photo2.jpg')

#         cls.newsfeed = Newsfeed.objects.create(
#             description='Test description',
#             user=cls.user
#         )
#         cls.newsfeed.photos.add(cls.photo1, cls.photo2)
#         cls.newsfeed.tags.add(cls.tag1, cls.tag2)
#         cls.newsfeed.likes.add(cls.user)

#     def test_newsfeed_model_str_method(self):
#         newsfeed = Newsfeed.objects.get(id=self.newsfeed.id)
#         self.assertEqual(
#             str(newsfeed),
#             f"{self.user}'s photos"
#         )

#     def test_newsfeed_model_description_field(self):
#         newsfeed = Newsfeed.objects.get(id=self.newsfeed.id)
#         self.assertEqual(newsfeed.description, 'Test description')

#     def test_newsfeed_model_user_foreign_key(self):
#         newsfeed = Newsfeed.objects.get(id=self.newsfeed.id)
#         self.assertEqual(newsfeed.user, self.user)

#     def test_newsfeed_model_photos_many_to_many_field(self):
#         newsfeed = Newsfeed.objects.get(id=self.newsfeed.id)
#         self.assertEqual(newsfeed.photos.count(), 2)
#         self.assertIn(self.photo1, newsfeed.photos.all())
#         self.assertIn(self.photo2, newsfeed.photos.all())

#     def test_newsfeed_model_likes_many_to_many_field(self):
#         newsfeed = Newsfeed.objects.get(id=self.newsfeed.id)
#         self.assertEqual(newsfeed.likes.count(), 1)
#         self.assertIn(self.user, newsfeed.likes.all())

#     def test_newsfeed_model_tags_many_to_many_field(self):
#         newsfeed = Newsfeed.objects.get(id=self.newsfeed.id)
#         self.assertEqual(newsfeed.tags.count(), 2)
#         self.assertIn(self.tag1, newsfeed.tags.all())
#         self.assertIn(self.tag2, newsfeed.tags.all())


# class UserInfoModelTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(username='testuser', password='testpassword')

#         cls.user_info = UserInfo.objects.create(
#             id=cls.user.id,
#             profile_photo='profile_photos/profile1.jpg',
#             biography='Test biography'
#         )
#         cls.user_info.subscriptions.add(cls.user)

#     def test_user_info_model_str_method(self):
#         user_info = UserInfo.objects.get(id=self.user_info.id)
#         self.assertEqual(
#             str(user_info),
#             f"Info about {self.user.username}"
#         )

#     def test_user_info_model_profile_photo_field(self):
#         user_info = UserInfo.objects.get(id=self.user_info.id)
#         self.assertEqual(user_info.profile_photo, 'profile_photos/profile1.jpg')

#     def test_user_info_model_biography_field(self):
#         user_info = UserInfo.objects.get(id=self.user_info.id)
#         self.assertEqual(user_info.biography, 'Test biography')

#     def test_user_info_model_subscriptions_many_to_many_field(self):
#         user_info = UserInfo.objects.get(id=self.user_info.id)
#         self.assertEqual(user_info.subscriptions.count(), 1)
#         self.assertIn(self.user, user_info.subscriptions.all())
