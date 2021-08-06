from taxonomy.models import Topic


def parse_search_terms(get_request):
    selected_topic_ids = None
    selected_topics = None
    for key, value in get_request.items():
        if key.startswith('topics'):
            if not selected_topic_ids:
                selected_topic_ids = []
            selected_topic_ids.append(int(value))
    text_search = get_request.get('text_search')
    if selected_topic_ids:
        selected_topics = Topic.objects.filter(pk__in=selected_topic_ids)
    return (selected_topics, text_search)
