from django.contrib import messages
from django.template import loader
from django.http import HttpResponse

from advertising import get_ad
from news.models import NewsPost
from news.helpers import parse_search_terms
from taxonomy.models import Topic


def front_page(request):
    """ View for the site's front page
        Returns all available newsposts, formatted like:
            cover_story: the newsposts with is_cover_story = True
            top_stories: the 3 most recent newsposts that are not cover story
            archive: the rest of the newsposts, sorted by most recent
    """
    template = loader.get_template('news/frontpage.html')
    cover_story = NewsPost.objects.filter(is_cover_story=True).first()
    all_stories = NewsPost.objects.filter(is_cover_story=False, active=True).order_by('-publish_date')[:8]

    top_stories = all_stories[:3]
    recent_stories = all_stories[3:]

    context = {
        'cover_story': cover_story,
        'top_stories': top_stories,
        'recent_stories': recent_stories,
    }

    return HttpResponse(template.render(context, request))


def newspost_detail(request, newspost_id):
    template = loader.get_template('news/newspost.html')
    newspost = NewsPost.objects.get(pk=newspost_id)
    context = {
        'newspost': newspost,
        'ad': get_ad()
    }
    return HttpResponse(template.render(context, request))


def archive(request):
    template = loader.get_template('news/archive.html')
    topics = Topic.objects.all().order_by('display_name')
    selected_topics, text_search_value = parse_search_terms(request.GET)
    news_archive = NewsPost.search(topics=selected_topics, text_value=text_search_value)
    context = {
        'news_archive': news_archive,
        'topics': topics,
        'text_search': request.GET.get('text_search'),
        'selected_topics': selected_topics,
        'searched': selected_topics or text_search_value,
        'selected_topics': selected_topics,
        'text_search_value': text_search_value,
    }

    return HttpResponse(template.render(context, request))
