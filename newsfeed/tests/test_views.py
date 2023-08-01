from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Newsfeed, UserInfo, Photo
from django.core.files.uploadedfile import SimpleUploadedFile


class NewsfeedViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.userinfo = UserInfo.objects.create(profile_photo='profile.jpg', biography='Test bio')
        self.userinfo.subscriptions.add(self.user)
        self.newsfeed = Newsfeed.objects.create(description='Test post', user=self.user)

    def test_index_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/newsfeed.html')
        self.assertContains(response, 'Test post')

    def test_index_unauthenticated_user(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/all_posts/')

    def test_index_userinfo_creation(self):
        UserInfo.objects.all().delete()
        self.client.login(username='testuser', password='testpassword')
        self.client.get(reverse('index'))
        self.assertEqual(UserInfo.objects.count(), 1)
        self.assertEqual(UserInfo.objects.first().subscriptions.first(), self.user)

    def test_index_with_no_subscriptions(self):
        self.userinfo.subscriptions.clear()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/newsfeed.html')


class AllPostsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.userinfo = UserInfo.objects.create(profile_photo='profile.jpg', biography='Test bio')
        self.userinfo.subscriptions.add(self.user)
        self.newsfeed = Newsfeed.objects.create(description='Test post', user=self.user)
        self.photo1 = Photo.objects.create(photo='photo1.jpg')
        self.photo2 = Photo.objects.create(photo='photo2.jpg')
        self.newsfeed.photos.add(self.photo1, self.photo2)

    def test_all_posts_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/all_posts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/all_posts.html')
        self.assertContains(response, 'Test post')
        self.assertContains(response, 'photo1.jpg')
        self.assertContains(response, 'photo2.jpg')

    def test_all_posts_view_custom_queryset(self):
        custom_newsfeed_objects = Newsfeed.objects.filter(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/all_posts/', {'newsfeed_objects': custom_newsfeed_objects})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/all_posts.html')
        self.assertContains(response, 'Test post')
        self.assertContains(response, 'photo1.jpg')
        self.assertContains(response, 'photo2.jpg')

    def test_all_posts_view_with_no_subscriptions(self):
        self.userinfo.subscriptions.clear()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/all_posts.html')
        self.assertNotContains(response, 'Test post')
        self.assertNotContains(response, 'photo1.jpg')
        self.assertNotContains(response, 'photo2.jpg')


class LikePhotoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.newsfeed = Newsfeed.objects.create(description='Test post', user=self.user)

    def test_like_photo_add_like(self):
        self.client.login(username='testuser', password='testpassword')
        data = {'like_info': f'{self.newsfeed.id}~{self.user.id}', 'next_url': '/home/'}
        response = self.client.post(reverse('like_photo'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.newsfeed.likes.count(), 1)
        self.assertTrue(self.newsfeed.likes.filter(id=self.user.id).exists())

    def test_like_photo_remove_like(self):
        self.newsfeed.likes.add(self.user)
        self.client.login(username='testuser', password='testpassword')
        data = {'like_info': f'{self.newsfeed.id}~{self.user.id}', 'next_url': '/home/'}
        response = self.client.post(reverse('like_photo'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.newsfeed.likes.count(), 0)
        self.assertFalse(self.newsfeed.likes.filter(id=self.user.id).exists())


@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class UploadViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_upload_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/upload.html')
        self.assertIn('current_username', response.context)
        self.assertIn('current_user_id', response.context)


@override_settings(DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
class UserSettingsViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.userinfo1 = UserInfo.objects.create(id=self.user1.id, profile_photo='photo1.jpg', biography='Bio 1')
        self.userinfo2 = UserInfo.objects.create(id=self.user2.id, profile_photo='photo2.jpg', biography='Bio 2')

    def test_user_settings_view_get_own_user(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('user_settings', args=['testuser1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings/settings.html')
        self.assertIn('current_username', response.context)
        self.assertIn('current_user_id', response.context)
        self.assertEqual(response.context['current_username'], 'testuser1')
        self.assertEqual(response.context['current_user_id'], self.user1.id)
        self.assertEqual(response.context['profile_photo'], 'photo1.jpg')
        self.assertEqual(response.context['biography'], 'Bio 1')

    def test_user_settings_view_get_other_user(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('user_settings', args=['testuser2']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/no_access_page.html')

    def test_user_settings_view_post(self):
        self.client.login(username='testuser1', password='testpassword')
        photo_content = b'Test photo content'
        photo = SimpleUploadedFile('test_photo.jpg', photo_content, content_type='image/jpeg')
        data = {
            'biography': 'Updated bio',
            'fullname': 'Updated Fullname',
            'profile_photo': photo,
        }
        response = self.client.post(reverse('user_settings', args=['testuser1']), data, format='multipart')
        self.assertEqual(response.status_code, 302)  # Redirect
        userinfo = UserInfo.objects.get(id=self.user1.id)
        self.assertEqual(userinfo.biography, 'Updated bio')
        user = User.objects.get(username='testuser1')
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Fullname')


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.userinfo1 = UserInfo.objects.create(id=self.user1.id, profile_photo='photo1.jpg', biography='Bio 1')

    def test_user_profile_view_with_newsfeed(self):
        Newsfeed.objects.create(description='Post 1', user=self.user1)
        Newsfeed.objects.create(description='Post 2', user=self.user1)
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.get(reverse('user_profile', args=['testuser1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/user_profile.html')
        self.assertIn('posts', response.context)
        self.assertTrue(response.context['posts'])
        self.assertEqual(len(response.context['posts']), 2)

    def test_user_profile_view_without_newsfeed(self):
        self.client.login(username='testuser2', password='testpassword')
        self.client.get('')
        response = self.client.get(reverse('user_profile', args=['testuser2']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'newsfeed/user_profile.html')
        self.assertIn('posts', response.context)
        self.assertTrue(response.context['posts'])
        self.assertEqual(len(response.context['posts']), 1)
        self.assertEqual(response.context['posts'][0]['author_username'], 'testuser2')
        self.assertEqual(response.context['posts'][0]['author_profile_photo'], 'default_photos/default_photo.png')
        self.assertEqual(response.context['posts'][0]['author_biography'], '')
        self.assertEqual(response.context['posts'][0]['author_first_name'], '')
        self.assertEqual(response.context['posts'][0]['author_last_name'], '')

    def test_user_profile_view_unauthenticated_user(self):
        response = self.client.get(reverse('user_profile', args=['testuser1']))
        self.assertEqual(response.status_code, 302)


class CreateUserInfoTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')

        self.userinfo2 = UserInfo.objects.create(id=self.user2.id, profile_photo='profile_photo2.jpg')

    def test_create_userinfo_success(self):
        self.client.login(username='user1', password='password1')
        self.client.get('')

        self.assertEqual(UserInfo.objects.count(), 3)
        self.assertIsNotNone(UserInfo.objects.get(id=self.user1.id))
        self.assertIsNotNone(UserInfo.objects.get(id=self.user3.id))
