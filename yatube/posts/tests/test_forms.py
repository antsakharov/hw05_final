from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Group, Post, Comment

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="test_user")
        cls.group = Group.objects.create(
            title='test_group',
            slug='test_slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='test_text',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_new_post(self):
        """Валидная форма создает запись в Post."""

        posts_count = Post.objects.count()
        form_data = {
            'text': PostFormTests.post.text,
            'group': PostFormTests.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:profile', kwargs={'username': self.user})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        post = Post.objects.latest('id')
        self.assertTrue(post.text == form_data['text'])
        self.assertTrue(post.group_id == form_data['group'])

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""

        posts_count = Post.objects.count()
        form_data = {
            'text': 'Просто текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:post_detail',
                              kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                id=PostFormTests.post.pk,
                text=form_data['text'],
                group=form_data['group'],
            ).exists()
        )

    def test_comment_form_non_auth(self):
        """Тестирование формы создания комментария"""
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Тестовый комментарий',
        }
        Comment.objects.create(
            author=self.user,
            text='Тестовый комментарий',
            post=self.post,

        )
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), comments_count + 1)

        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый комментарий',
            ).exists()
        )
        added_comment = response.context["comments"][0]
        self.assertEqual(added_comment.post, self.post)
        self.assertEqual(added_comment.author, self.user)
        self.assertEqual(added_comment.text, form_data["text"])
