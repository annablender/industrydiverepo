code_reviews = [
    # {
    #     'title': 'Site front page',
    #     'description': 'There are several bugs on the front page of the Wavepool site. Fix these bugs by editing the front_page.html template file and the front_page view in views.py. Submit a pull request for a branch titled "yourlastname_yourfirstname_front_page_fixes"',  # noqa
    #     'acceptance_criteria': [
    #         'The newspost designated as the cover story should appear in the cover story box',
    #         'The 3 most recent stories, excluding the cover story, should be displayed under "top stories", ordered by most recent first',  # noqa
    #         'All news posts that do not appear as the cover story or as top stories should be listed in the archive, ordered by most recent first',  # noqa
    #         'Newspost teasers should be properly rendered as HTML',
    #     ],
    #     'pull_request': 'https://github.com/industrydive/wavepool/pull/2',
    # },
]

code_prompts = [
    {
        'title': 'Bug in News Post teaser',
        'description': '''
            There is a logical error in the handling of News Post teaser field - the current logic uses the first 150
            characters of the News Post body as the teaser. If this part of the News Post contains HTML tags that are
            not closed by the end of the character cut off, then it can mess up the HTML of the whole page. An example
            of this can be seen with the News Post "Regeneron antibody cuts risk of COVID-19 death in UK study". You
            can reproduce the behavior by setting this News Post to <code>active</code> and viewing the Front Page or
            the Archive Page. Design and implement a solution so that News Post teasers can be custom set by editors
            or so that they print safely when included in feed lists.
        ''',
        'acceptance_criteria': [
            'News posts with HTML tags do not disrupt the HTML structure of the wavepool site'
        ],
        'objectives': [
            'Demonstrate ability to comprehend and reproduce a bug report',
            'Demonstrate ability to design a solution that solves a minor bug',
        ],
        'relevant_screenshots': [
            {
                'source': 'teaser-html-bug.png',
                'text': 'This newspost has unclosed HTML in the teaser and breaks the page'
            },
        ],
        'difficulty_out_of_3': 1,
    },
    {
        'title': 'Customizable News Post Ads',
        'description': '''
        The sales team currently sells a single advertisement to a client for the whole site.
        The HTML for this ad is periodically updated manually via engineering team support tickets.
        The Sales Team wants the ability to create their own ads using the CMS and assign them to specific news posts
        in order to maximize revenue. An <code>advertising</code> app already exists for you to build off of and the
        existing ads can be found in a dictionary under <code>advertising/__init__.py</code>
        ''',
        'objectives': [
            'Demonstrate ability to comprehend user acceptance criteria',
            'Demonstrate ability to design and build Django Models',
            'Demonstrate ability to set up standard Django CMS admin pages'
        ],
        'acceptance_criteria': [
            'A Sales Team member can access a set of standard admin pages in the CMS to create advertisements',
            'For each advertisement they should be able to upload a client logo, a link that the ad should open to, and the ad\'s text',  # noqa
            'Each advertisement should appear on the news post that it is sold for',
            'The Sales Team might sell more than one news post slot to a client at a time, so they should be able to set a single ad to multiple posts',  # noqa
            'The Sales Team might sell no ads for a particular news post, in which case the Industry Dive "House Ad" should show by default',  # noqa
        ],
        'relevant_screenshots': [
            {
                'source': 'client-ad.png',
                'text': 'A client ad for a news post is displayed when set to the given news post'
            },
            {
                'source': 'default-ad.png',
                'text': 'The Industry Dive "House ad" shows when no ad is assigned to a given news post'
            },
        ],
        'difficulty_out_of_3': 2,
    },
    {
        'title': 'Cover Story CMS Functionality',
        'description': '''
            Currently, there is no way to stop a CMS user from setting more than one story as the cover story. There is
            also nothing that alerts the Editorial Team if no story is currently set as a cover story.
            The front page template is not set up to allow for these situations. The Editorial team has requested a
            couple of features to address this poor user experience:</p>
            <ol>
            <li>Update the CMS so that if a news post is set as the cover story, other news posts that are set as the
            cover story get un-set.</li>
            <li>Add an alert message on the news post list page so that Editors can see when when there is no current
            cover story.</li>
            </ol>
        ''',
        'objectives': [
            'Demonstrate ability to comprehend user acceptance criteria',
            'Demonstrate ability to override or extend Django methods',
            'Demonstrate ability to customize Django CMS admin pages',
        ],
        'acceptance_criteria': [
            'Only one story can be saved as the cover story using the <code>is_cover_story</code> field',
            'Editors see an alert on the news post admin list page when there is cover story set'
        ],
        'relevant_screenshots': [
            {
                'source': 'no-cover-story-alert.png',
                'text': 'Alert should be present when there is no cover story set'
            },
        ],
        'difficulty_out_of_3': 3,
    },
    {
        'title': 'Make Archive Search Behave Like a Single Page App',
        'description': '''
            <p>The Archive search page works great! However, to improve the user experience, the UX team has requested
            it to be refactored so that it behaves like a single page app. The front end implementation is totally up
            to you - it can be vanilla Javascript, JQuery, React, Angular, etc. </p>
            <p>An API has been provided at <code>/api/v1/news/</code> to help. It works the same way as the archive
            page search function. So, <code>/api/v1/news/?/topics_12=12&topics_20=20&text_search=walmart</code> should
            provide the same results as <code>/news/archive/?topics_12=12&topics_20=20&text_search=walmart</code>.</p>
        ''',
        'acceptance_criteria': [
            'When a user inputs anything in the search fields, the page should switch to the search results format',
            'When a user inputs anything in the search fields, the feed should list any stories matching the search '
            'criteria without the user needing to press "Search"',
        ],
        'objectives': [
            'Demonstrate ability to comprehend user acceptance criteria',
            'Demonstrate ability to design a front-end solution to a UX request',
            'Demonstrate ability to design a front-end solution that integrates with an existing Django application',
        ],
        'relevant_screenshots': [
            {
                'source': 'archive-view.png',
                'text': 'Archive page with no search fields set'
            },
            {
                'source': 'search-results-view.png',
                'text': 'Archive page with search results rendered'
            },
        ],
        'difficulty_out_of_3': 3,
    },
]
