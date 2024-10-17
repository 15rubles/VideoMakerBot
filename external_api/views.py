import json
from functools import wraps

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from external_api.apis.youtube_api import YouTubeController

@require_http_methods(["GET"])
def youtube_api_basic_info(request):
    link = request.GET.get('link')
    if not link:
        return JsonResponse({'error': 'link is required'}, status=400)

    yt = YouTubeController.get_youtube_video(link)

    video_details = {
        'title': yt.title,
        'description': yt.description,
        'publish_date': yt.publish_date.isoformat() if yt.publish_date else None,
        'views': yt.views,
        'length': yt.length,
        'author': yt.author,
        'thumbnail_url': yt.thumbnail_url,
        'streaming_data': yt.streaming_data,  # contains formats and other streaming details
        'video_id': yt.video_id,  # Adaptive streaming options
        'keywords': yt.keywords,
    }

    video_details_json = json.dumps(video_details, indent=4)
    return HttpResponse(video_details_json, content_type='text/html')
