from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from .models import Newsfeed, Tags, UserInfo, Photo
from django.contrib.auth.models import User


def index(request):
    """
    View function to display the user's newsfeed based on their subscriptions.
    If the user is not authenticated, they are redirected to the 'all_posts' page.
    """
    if not (user := request.user).is_authenticated:
        return redirect('/all_posts/')
    try:
        userinfo = UserInfo.objects.filter(id=user.id)[0]
    except IndexError:
        create_userinfo()
        userinfo = UserInfo.objects.filter(id=user.id)[0]

    sub_list = [i.id for i in userinfo.subscriptions.all()]
    newsfeed_objects = []

    for post in Newsfeed.objects.all():
        if post.user_id in sub_list:
            newsfeed_objects.append(post)

    return all_posts(request, newsfeed_objects=newsfeed_objects,
                     template='newsfeed/newsfeed.html',
                     view_style='newsfeed')


def all_posts(request, newsfeed_objects=None, template='newsfeed/all_posts.html', view_style='all_posts'):
    """
    This function is used to display the newsfeed. It performs the following steps:
        1. Calls the create_userinfo function.
        2. Initializes an empty list, photo_info, to store information about each newsfeed object.
        3. Iterates through each newsfeed object in the provided newsfeed_objects queryset:
           - Retrieves various information such as post ID, author username, photos, description, author first name,
             author last name, author profile photo, author biography, number of photos, number of likes,
             tags, and whether the post is liked by the current user.
           - Appends the gathered information to the photo_info list.
        4. Creates a context dictionary with the 'posts' key set to the photo_info list.
        5. Adds additional information to the context dictionary if the current user is authenticated.
           - Adds the current username and user ID to the context.
        6. Renders the specified template using the context.
    """
    create_userinfo()
    current_user = request.user if request.user.is_authenticated else None

    if newsfeed_objects is None:
        newsfeed_objects = Newsfeed.objects.all()

    photo_info = []
    for post in newsfeed_objects[::-1]:
        author = User.objects.filter(id=post.user_id)[0]
        photo_info.append({'post_id': post.id,
                           'photos': [photo.photo for photo in post.photos.all()],
                           'description': post.description,
                           'author_id': author.id,
                           'author_username': author.username,
                           'author_first_name': author.first_name,
                           'author_last_name': author.last_name,
                           'author_profile_photo': UserInfo.objects.filter(id=author.id)[0].profile_photo,
                           'author_biography': UserInfo.objects.filter(id=author.id)[0].biography,
                           'number_of_photos': len(post.photos.all()),
                           'likes': post.likes.all().count(),
                           'tags': ' '.join([f'#{j.name}' for j in post.tags.all()]),
                           'is_liked_by_current_user':
                               current_user in post.likes.all() if request.user.is_authenticated else False
                           })

    context = {'posts': photo_info, 'view_style': view_style}

    if current_user:
        context['current_username'] = current_user.username
        context['current_user_id'] = current_user.id
        if view_style == 'user_profile':
            author = User.objects.filter(id=context['posts'][0]['author_id'])[0]
            context['is_subscribed'] = author in UserInfo.objects.filter(id=current_user.id)[0].subscriptions.all()
            context['subscribers_count'] = -1
            for userinfo in UserInfo.objects.all():
                context['subscribers_count'] += 1 if author in userinfo.subscriptions.all() else 0

    return render(request, template, context=context)


def like_photo(request):
    """
    Function for handling photo like/unlike requests.

    Updates the likes for a newsfeed item based on the provided POST data. If
    the user has already liked the photo, their like is removed. Otherwise, a
    new like is added. The function then redirects the user to the home page.
    """
    like_info = request.POST['like_info']
    newsfeed_id, user_id = like_info.split('~')

    if User.objects.filter(id=user_id)[0] in Newsfeed.objects.filter(id=newsfeed_id)[0].likes.all():
        Newsfeed.objects.filter(id=newsfeed_id)[0].likes.remove(User.objects.filter(id=user_id)[0])
    elif User.objects.filter(id=user_id)[0] not in Newsfeed.objects.filter(id=newsfeed_id)[0].likes.all():
        Newsfeed.objects.filter(id=newsfeed_id)[0].likes.add(User.objects.filter(id=user_id)[0])

    return redirect(request.POST['next_url'])


def change_tags(request, other_tags=None, other_newsfeed_id=None):
    """
    Function for handling newsfeed tag changes.

    Updates the tags for a newsfeed item based on the provided tags or POST
    data. If the tags do not exist in the database, they are created. The
    function then updates the tags for the newsfeed item and redirects the user
    to the home page.

    other_tags and other_newsfeed_id is optional string to use function
    instead of the POST tags. Default is None.
    """
    if other_tags is not None:
        tags, newsfeed_id = other_tags, other_newsfeed_id
    else:
        tags, newsfeed_id = request.POST['tags'].split(' '), request.POST['newsfeed_id']
    for tag in tags:
        if tag[1:] not in [tag_.name for tag_ in Tags.objects.all()]:
            Tags.objects.create(name=tag[1:])

    for tag in Newsfeed.objects.filter(id=int(newsfeed_id))[0].tags.all():
        Newsfeed.objects.filter(id=int(newsfeed_id))[0].tags.remove(tag)

    for tag in tags:
        Newsfeed.objects.filter(id=int(newsfeed_id))[0].tags.add(Tags.objects.filter(name=tag[1:])[0].id)

    return redirect('/')


def upload(request):
    """
    This function is used to add a new photo to the newsfeed. It handles both GET and POST requests.
    - If the request method is GET, it renders the 'newsfeed/upload.html' template.
    - If the request method is POST, it retrieves the photo URL, description, tags, and user ID from the request.
    It creates a new newsfeed item using the provided information and calls the change_tags function
    to add the provided tags to the newsfeed item. Finally, it redirects the user to the home page.
    """

    if request.method == 'GET':
        context = dict()

        if request.user.is_authenticated:
            context['current_username'] = User.objects.filter(id=request.user.id)[0].username
            context['current_user_id'] = request.user.id

        return render(request, 'newsfeed/upload.html', context=context)
    elif request.method == 'POST':
        photo_paths = []
        for file in request.FILES.getlist('photo'):
            photo_paths.append(default_storage.save('newsfeed_photos/' + file.name, ContentFile(file.read())))

        new_post = Newsfeed.objects.create(description=request.POST['description'], user=request.user)

        for photo in photo_paths:
            new_photo = Photo.objects.create(photo=photo)
            new_post.photos.add(new_photo)

        change_tags(request=request, other_tags=request.POST['tags'].split(' '), other_newsfeed_id=new_post.id)

        return redirect('/')


def user_settings(request, username):
    """
    This function handles the user settings for the specified username. It performs the following steps:
        1. Calls the create_userinfo function.
        2. If the username is 'new_user', it redirects the user to the settings page for the currently logged-in user.
        3. Retrieves the user object with the specified username. If the user does not exist, a 404 error is raised.
        4. If the username does not match the username of the currently logged-in user:
           - Creates a context dictionary to pass additional information to the template.
           - Checks if the current user is authenticated.
           - Adds the current username and user ID to the context dictionary.
           - Renders the 'newsfeed/no_access_page.html' template with the context.
    """
    create_userinfo()
    if request.method == 'GET':
        create_userinfo()
        if username == 'new_user':
            return redirect('/user/settings/' + request.user.username)
        user = get_object_or_404(User, username=username)

        if username != request.user.username:
            return render(request, 'newsfeed/no_access_page.html')

        context = {'current_username': user.username,
                   'current_user_id': user.id,
                   'profile_photo': UserInfo.objects.filter(id=user.id)[0].profile_photo,
                   'biography': UserInfo.objects.filter(id=user.id)[0].biography,
                   'fullname': f"{user.first_name} {user.last_name}"}

        return render(request, 'settings/settings.html', context=context)
    elif request.method == 'POST':
        userinfo = UserInfo.objects.filter(id=User.objects.filter(username=username)[0].id)[0]

        if not request.FILES.getlist('profile_photo'):
            userinfo.profile_photo = "default_photos/default_photo.png"
        else:
            file = request.FILES.getlist('profile_photo')[0]
            path = default_storage.save('profile_photos/' + file.name, ContentFile(file.read()))
            userinfo.profile_photo = path

        userinfo.biography = request.POST['biography']
        userinfo.save()

        user = request.user
        user.first_name = (fullname := request.POST['fullname'].strip()).split(' ')[0]
        user.last_name = ' '.join(fullname.split(' ')[1:])
        user.save()

        return redirect(f'/user/settings/{request.user.username}')


def user_profile(request, username):
    """
     This function is used to display the user profile for the specified username. It performs the following steps:
        1. Checks if there are any newsfeed objects associated with the user ID of the specified username.
           - If there are, it calls the index function with the appropriate parameters to display the user's newsfeed.
           - The template used for rendering is 'newsfeed/user_profile.html'.
        2. If there are no newsfeed objects associated with the user ID, it retrieves the user object with the specified username.
           - Creates a dictionary with the necessary information for rendering the user profile.
           - The dictionary includes the username, profile photo, biography, first name, and last name of the user.
           - The context dictionary is created with the 'posts' key set to the list of profile information.
        3. Adds additional information to the context dictionary if the current user is authenticated.
           - Adds the current username and user ID to the context.
        4. Sets the 'user_has_no_photos' key in the context dictionary to True.
        5. Renders the 'newsfeed/user_profile.html' template with the context.
    """
    author = get_object_or_404(User, username=username)

    if Newsfeed.objects.filter(user_id=author):
        return all_posts(request,
                         newsfeed_objects=Newsfeed.objects.filter(user_id=author),
                         template='newsfeed/user_profile.html',
                         view_style='user_profile'
                         )
    else:
        current_user = request.user if request.user.is_authenticated else None

        context = {'posts': [{
            'author_id': author.id,
            'author_username': username,
            'author_profile_photo': UserInfo.objects.filter(id=author.id)[0].profile_photo,
            'author_biography': UserInfo.objects.filter(id=author.id)[0].biography,
            'author_first_name': author.first_name,
            'author_last_name': author.last_name,
        }]}

        if current_user:
            context['current_username'] = current_user.username
            context['current_user_id'] = current_user.id
            context['is_subscribed'] = author in UserInfo.objects.filter(id=current_user.id)[0].subscriptions.all()
            context['subscribers_count'] = -1
            for userinfo in UserInfo.objects.all():
                context['subscribers_count'] += 1 if author in userinfo.subscriptions.all() else 0

        return render(request, 'newsfeed/user_profile.html', context)


def subscribe(request):
    """
    View function to handle user subscription.
    Extracts the user IDs from the request URL and subscribes/unsubscribes the user to/from another user.
    """
    user_id, user_to_subscribe_id = request.get_full_path().split('?')[1].split('_')
    user, user_to_subscribe = User.objects.filter(id=user_id)[0], User.objects.filter(id=user_to_subscribe_id)[0]

    if str(user_id) != str(request.user.id):
        return render(request, 'newsfeed/no_access_page.html')

    if user_to_subscribe in list((userinfo := UserInfo.objects.filter(id=user.id)[0]).subscriptions.all()):
        userinfo.subscriptions.remove(user_to_subscribe)
    else:
        userinfo.subscriptions.add(user_to_subscribe)

    return redirect("user_profile", username=user_to_subscribe.username)


def create_userinfo():
    """
    This function creates a UserInfo object for each User object in
    the database that does not have a corresponding UserInfo object.
    The profile_photo attribute of the created UserInfo objects is
    set to the default.
    """

    for user in User.objects.all():
        if user.id not in [i.id for i in UserInfo.objects.all()]:
            userinfo = UserInfo.objects.create(id=user.id, profile_photo="default_photos/default_photo.png")
            userinfo.subscriptions.add(user)
