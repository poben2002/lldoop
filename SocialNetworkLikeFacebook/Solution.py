import uuid
from datetime import datetime
from collections import defaultdict


class User:
    def __init__(self, name, email, password):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password  # In real systems, use hashing
        self.profile = {
            "bio": "",
            "interests": [],
            "profile_picture": None,
        }
        self.friends = set()
        self.incoming_requests = set()
        self.outgoing_requests = set()
        self.posts = []
        self.notifications = []

    def update_profile(self, bio=None, interests=None, profile_picture=None):
        if bio: self.profile["bio"] = bio
        if interests: self.profile["interests"] = interests
        if profile_picture: self.profile["profile_picture"] = profile_picture


class Post:
    def __init__(self, user_id, content, media=None, visibility='public'):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.content = content
        self.media = media
        self.likes = set()
        self.comments = []
        self.visibility = visibility  # public, friends-only, private

    def add_like(self, user_id):
        self.likes.add(user_id)

    def add_comment(self, comment):
        self.comments.append(comment)


class Comment:
    def __init__(self, user_id, content):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.content = content
        self.timestamp = datetime.now()


class Notification:
    def __init__(self, content):
        self.id = str(uuid.uuid4())
        self.content = content
        self.timestamp = datetime.now()


class SocialNetwork:
    def __init__(self):
        self.users = {}       # user_id -> User
        self.posts = {}       # post_id -> Post
        self.email_map = {}   # email -> user_id (for login)

    def register_user(self, name, email, password):
        if email in self.email_map:
            raise ValueError("Email already registered.")
        user = User(name, email, password)
        self.users[user.id] = user
        self.email_map[email] = user.id
        return user

    def login_user(self, email, password):
        user_id = self.email_map.get(email)
        if not user_id: return None
        user = self.users[user_id]
        return user if user.password == password else None

    def send_friend_request(self, from_id, to_id):
        from_user = self.users[from_id]
        to_user = self.users[to_id]
        if to_id not in from_user.friends:
            from_user.outgoing_requests.add(to_id)
            to_user.incoming_requests.add(from_id)
            to_user.notifications.append(Notification(f"{from_user.name} sent you a friend request."))

    def accept_friend_request(self, from_id, to_id):
        from_user = self.users[from_id]
        to_user = self.users[to_id]
        if from_id in to_user.incoming_requests:
            from_user.friends.add(to_id)
            to_user.friends.add(from_id)
            from_user.outgoing_requests.discard(to_id)
            to_user.incoming_requests.discard(from_id)

    def create_post(self, user_id, content, media=None, visibility='public'):
        post = Post(user_id, content, media, visibility)
        self.posts[post.id] = post
        self.users[user_id].posts.append(post)
        return post

    def get_newsfeed(self, user_id):
        user = self.users[user_id]
        friends = user.friends
        all_posts = []

        for uid in friends.union({user_id}):  # include user's own posts
            for post in self.users[uid].posts:
                if post.visibility in ['public', 'friends-only'] or post.user_id == user_id:
                    all_posts.append(post)

        return sorted(all_posts, key=lambda p: p.timestamp, reverse=True)

    def like_post(self, user_id, post_id):
        post = self.posts[post_id]
        post.add_like(user_id)
        self.users[post.user_id].notifications.append(Notification(f"{self.users[user_id].name} liked your post."))

    def comment_on_post(self, user_id, post_id, content):
        post = self.posts[post_id]
        comment = Comment(user_id, content)
        post.add_comment(comment)
        self.users[post.user_id].notifications.append(Notification(f"{self.users[user_id].name} commented on your post."))

    def get_notifications(self, user_id):
        return self.users[user_id].notifications
