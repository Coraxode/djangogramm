# DjangoGramm
***
This is a Django-based application that allows users to create posts, follow other users, like posts, and view personalized newsfeeds based on their subscriptions.

__Usage__
* configure ```.env``` file
* run application using docker compose: 
  ```docker compose up```


__Features__
* __User authentication__: Users can register and log in to the application using their email and password.
* __Newsfeed__: The index function displays the user's newsfeed based on their subscriptions. Users can view posts from other users they follow.
* __Create and upload posts__: Users can create and upload posts to the newsfeed. Posts can include descriptions, multiple photos and tags.
* __User profiles__: Each user has a profile page displaying their posts and profile information. Users can view their own profiles and those of other users.
* __Likes and Tags__: Users can like and unlike posts from other users. Posts can have tags, allowing for better categorization.
* __User Settings__: Users can update their profile information, such as their profile photo and biography.
* __Subscription__: Users can subscribe and unsubscribe to other users. The newsfeed will include posts from users the current user is subscribed to.