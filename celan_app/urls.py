from django.urls import path
from celan_app.views.user_view import LogoutView
from celan_app.views.collection_view import CollectionView
from celan_app.views.toc_verse_view import TocVerseView
from celan_app.views.verse_view import VerseView

urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("collection/", CollectionView.as_view(), name="collection"),
    path(
        "collection/<int:collection_pk>/verses/toc/",
        TocVerseView.as_view(),
        name="collection_verses_toc",
    ),
    path("verse/<int:verse_id>/", VerseView.as_view(), name="verse"),
]
