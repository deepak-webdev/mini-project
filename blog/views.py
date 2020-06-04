from udemy import *
import json
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Post
from isodate import parse_duration
# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def button(request):
    return render(request, 'blog/home.html')


def home(request):
    Client = PyUdemy()
    data = Client.get_courseslist(page=1)
    data2 = json.loads(data)
    finaldata = data2['results']
    image_list = []
    url_list = []
    prices = []
    title_list = []
    instructor_list = []
    headline = []
    for x in range(len(finaldata)):

        title_list.append(finaldata[x]['title'])
        url_list.append('https://www.udemy.com' + finaldata[x]['url'])
        image_list.append(finaldata[x]['image_480x270'])
        headline.append(finaldata[x]['headline'])
        prices.append(finaldata[x]['price'])
        instructor_list.append(
            finaldata[x]['visible_instructors'][0]['display_name'])
        CourseInfo = zip(title_list, url_list, image_list,
                         headline, prices, instructor_list)

    return render(request, 'blog/home.html', {'CourseInfoData': CourseInfo})


def youtube(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos': videos
    }
    return render(request, 'blog/youtube.html', context)
