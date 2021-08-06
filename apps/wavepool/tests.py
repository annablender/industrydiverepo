import random
import string

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from wavepool.models import NewsPost, DIVESITE_SOURCE_NAMES


class TestBase(TestCase):
    fixtures = ['test_fixture', ]

    def _clean_text(self, text):
        return text.replace('\n', '').replace('\t', '')

    def _random_string(self, length):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(length))

    def _login_user(self):
        password = self._random_string(12)
        username = self._random_string(6)
        user = User.objects.create_superuser(
            username,
            '%s@industrydive.com' % username,
            password
        )
        user.save()
        client = self.client
        client.login(username=username, password=password)


class NewsPostDetail(TestBase):

    def test_newspost_page_title_attribute(self):
        """ Very that each newspost rendered at its unique URL displays the correct content
        """
        newsposts = NewsPost.objects.all()
        for newspost in newsposts:
            expected_title_tag_text = '{} | Wavepool | Industry Dive'.format(newspost.title)
            page = self.client.get(newspost.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            title_tag_text = page_html.title.text
            self.assertEqual(expected_title_tag_text, title_tag_text)

    def test_newspost_page_content(self):
        """ Very that each newspost rendered at its unique URL displays the correct content
        """
        newsposts = NewsPost.objects.all()
        for newspost in newsposts:
            page = self.client.get(newspost.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            rendered_title = page_html.find('h1', {'id': 'newspost-title'}).text
            rendered_body = page_html.find('div', {'id': 'newspost-body'}).text
            newspost_body = BeautifulSoup(newspost.body, 'html.parser').text
            self.assertEqual(rendered_title, newspost.title)
            self.assertEqual(self._clean_text(rendered_body), self._clean_text(newspost_body))

    def test_newspost_body_render(self):
        """ Verify that newsposts rendered at their URL do not display raw HTML to the screen
        """
        newsposts = NewsPost.objects.all()
        for newspost in newsposts:
            page = self.client.get(newspost.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            self.assertNotIn('<p>', page_html.text)

    def test_visitor_not_sees_edit_link(self):
        """ Verify that a visitor (non-logged in CMS user) cannot see the "edit" link on newspost pages
        """
        newsposts = NewsPost.objects.all()
        for newspost in newsposts:
            page = self.client.get(newspost.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            edit_link = page_html.find('a', {'id': 'edit-link'})
            self.assertIsNone(edit_link)

    def test_cms_user_sees_edit_link(self):
        """ Verify that a logged in CMS user sees the edit link on newspost pages and that it links to the correct change form
        """
        self._login_user()
        newsposts = NewsPost.objects.all()
        for newspost in newsposts:
            page = self.client.get(newspost.url)
            page_html = BeautifulSoup(page.content, 'html.parser')
            edit_link = page_html.find('a', {'id': 'edit-link'})
            edit_url = edit_link['href']
            self.assertEqual(edit_url, reverse('admin:wavepool_newspost_change', args=[newspost.pk]))

    def test_divesite_display_name(self):
        """ Verify that the source_divesite_name property of newspost returns the correct dive site for display
        """
        for short_name, expected_display_name in DIVESITE_SOURCE_NAMES.items():
            newspost = NewsPost(
                title='Man Bites Dog!',
                body='asdf',
                source='https://www.{}.com/asdf-asdf-asdf'.format(short_name)
            )
            newspost.save()
            newspost_divesite_name = newspost.source_divesite_name
            self.assertEqual(newspost_divesite_name, expected_display_name)

    def test_newspost_unique_urls(self):
        """ Verify that each newspost has a unique URL accessed via NewsPost.url
        """
        newsposts = NewsPost.objects.all()
        unique_newspost_urls = []
        for newspost in newsposts:
            self.assertNotIn(newspost.url, unique_newspost_urls)
            unique_newspost_urls.append(newspost.url)


class SiteFrontPage(TestBase):

    def test_cover_story_placement(self):
        """ Verify that the story designated as the cover story appears in the cover story box on the front page
        """
        cover_story = NewsPost.objects.all().order_by('?').first()
        cover_story.is_cover_story = True
        cover_story.save()

        front_page = self.client.get('')
        front_page_html = BeautifulSoup(front_page.content, 'html.parser')

        cover_story_div = front_page_html.find('div', {'id': 'coverstory'})
        cover_story_id = int(cover_story_div['data-newspost-id'])

        self.assertEqual(cover_story_id, cover_story.pk)

    def test_top_stories(self):
        """ Verify that the top stories section contains the 3 most recent stories, excluding the cover story
        """
        latest_four_stories = NewsPost.objects.all().order_by('-publish_date')[:4]
        cover_story = latest_four_stories[2]
        cover_story.is_cover_story = True
        cover_story.save()

        top_stories = [latest_four_stories[0], latest_four_stories[1], latest_four_stories[3], ]

        front_page = self.client.get('')
        front_page_html = BeautifulSoup(front_page.content, 'html.parser')

        rendered_top_stories = front_page_html.find_all('div', {'class': 'topstory'})
        self.assertEqual(len(rendered_top_stories), 3)

        top_story_1 = front_page_html.find(
            'div', {'class': 'topstory', 'data-top-story-placement': '1', }
        )
        top_story_1_id = int(top_story_1['data-newspost-id'])

        top_story_2 = front_page_html.find(
            'div', {'class': 'topstory', 'data-top-story-placement': '2', }
        )
        top_story_2_id = int(top_story_2['data-newspost-id'])

        top_story_3 = front_page_html.find(
            'div', {'class': 'topstory', 'data-top-story-placement': '3', }
        )
        top_story_3_id = int(top_story_3['data-newspost-id'])

        self.assertEqual(top_story_1_id, top_stories[0].pk)
        self.assertEqual(top_story_2_id, top_stories[1].pk)
        self.assertEqual(top_story_3_id, top_stories[2].pk)

    def test_archive_stories(self):
        """ Verify that the archived stories section contains all newsposts that are not the cover story or top stories
        """
        all_stories = NewsPost.objects.all().order_by('-publish_date')
        cover_story = all_stories[7]
        cover_story.is_cover_story = True
        cover_story.save()

        top_stories = [all_stories[0], all_stories[1], all_stories[2]]
        archive_stories = []
        for story in all_stories:
            if story not in top_stories and story != cover_story:
                archive_stories.append(story)

        front_page = self.client.get('')
        front_page_html = BeautifulSoup(front_page.content, 'html.parser')
        archive_story_divs = front_page_html.find_all('div', {'class': 'archived-story'})
        self.assertEqual(len(archive_story_divs), len(archive_stories))
        for div in archive_story_divs:
            story_id = int(div['data-archive-story-id'])
            self.assertIn(story_id, [s.id for s in archive_stories])

    def test_newspost_teaser_render(self):
        """ Verify that the teasers on the front page do not contain raw HTML printed to the screen
        """
        front_page = self.client.get('')
        front_page_html = BeautifulSoup(front_page.content, 'html.parser')
        teaser_divs = front_page_html.find_all('div', {'class': 'newspost-teaser'})
        for teaser in teaser_divs:
            self.assertNotIn('<p>', teaser.text)


class CmsPage(TestBase):
    fixtures = ['test_fixture', ]

    def _get_news_list_page_rows(self):
        self._login_user()
        list_page_url = reverse('admin:wavepool_newspost_changelist')
        list_page = self.client.get(list_page_url)
        page_html = BeautifulSoup(list_page.content, 'html.parser')
        list_table = page_html.find('table', {'id': 'result_list'})
        admin_rows = list_table.tbody.find_all('tr')
        return admin_rows

    def test_title_shows_on_list_page(self):
        """ Verify that CMS users can identify newsposts on the changelist page by seeing the newspost titles
        """
        admin_rows = self._get_news_list_page_rows()
        for row in admin_rows:
            resolved_admin_url = resolve(row.find('a')['href'])
            obj_id = resolved_admin_url.kwargs['object_id']
            newspost = NewsPost.objects.get(pk=obj_id)
            self.assertIn(newspost.title, row.text)

    def test_displayed_in_order(self):
        """ Verify that CMS users see newsposts on the changelist page ordered by most recent first
        """
        admin_rows = self._get_news_list_page_rows()
        last_pubdate = None
        for row in admin_rows:
            resolved_admin_url = resolve(row.find('a')['href'])
            obj_id = resolved_admin_url.kwargs['object_id']
            newspost = NewsPost.objects.get(pk=obj_id)
            if last_pubdate:
                self.assertTrue(newspost.publish_date <= last_pubdate)
            last_pubdate = newspost.publish_date

    def test_only_one_cover_story(self):
        """ Verify that when a CMS user sets an newspost as the cover story, the previously saved cover story is set False
        """
        self._login_user()
        newsposts = NewsPost.objects.all()

        old_cover_story_newspost = newsposts[2]
        old_cover_story_newspost.is_cover_story = True
        old_cover_story_newspost.save()

        new_cover_story_newspost = newsposts[3]
        new_cover_story_newspost_change_url = reverse(
            'admin:wavepool_newspost_change', args=[new_cover_story_newspost.pk]
        )
        post_data = {
            'title': new_cover_story_newspost.title,
            'publish_date': new_cover_story_newspost.publish_date,
            'body': new_cover_story_newspost.body,
            'source': new_cover_story_newspost.source,
            'is_cover_story': 'on',
        }
        self.client.post(new_cover_story_newspost_change_url, post_data)

        new_cover_story_newspost = NewsPost.objects.get(pk=new_cover_story_newspost.pk)
        self.assertTrue(new_cover_story_newspost.is_cover_story)

        old_cover_story_newspost = NewsPost.objects.get(pk=old_cover_story_newspost.pk)
        self.assertFalse(old_cover_story_newspost.is_cover_story)
