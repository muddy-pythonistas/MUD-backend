from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('get_map', api.get_map),
    url('grab_item', api.grab_item),
    url('drop_item', api.drop_item)
]