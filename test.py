import wordcloud

wc = WordCloud(
    label_options=dict(
        font_size=40,
        padding=(10, 10),
    ),
    label_cls='CloudLabel',
    words = (
        'Kivy',
        'Open',
        'source',
        'Python',
        'library',
        'for',
        'rapid',
        'development',
        'of',
        'applications',
        'that',
        'make',
        'use',
        'innovative',
        'user',
        'interfaces',
        'such',
        'as',
        'multi',
        'touch',
        'apps',
    )
)
wc.bind(
    on_post_populate=wc.animate_random_word,
    on_pre_populate=wc.cancel_animate_random_word,
)
root.add_widget(wc)