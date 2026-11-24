import os
import re
import subprocess
import tempfile
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile
from .models import Video, WatchLog
from .forms import VideoUploadForm, VideoNoteForm

GOAL_SECONDS = 10 * 60  # gündəlik hədəf: 10 dəqiqə


def srt_to_vtt(srt_content):
    vtt_content = "WEBVTT\n\n" + srt_content.replace(',', '.')
    vtt_content = re.sub(r'^\d+\s*$', '', vtt_content, flags=re.MULTILINE)
    return vtt_content


def generate_thumbnail(video):
    video_path = video.file.path
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [
                'ffmpeg', '-y',
                '-i', video_path,
                '-ss', '00:00:03',
                '-frames:v', '1',
                '-vf', 'scale=320:-1',
                tmp_path,
            ],
            capture_output=True,
            timeout=30,
        )
        if result.returncode == 0 and os.path.getsize(tmp_path) > 0:
            with open(tmp_path, 'rb') as f:
                base_name = os.path.splitext(os.path.basename(video.file.name))[0]
                video.thumbnail.save(f"{base_name}.jpg", ContentFile(f.read()), save=True)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def get_video_duration(video_path):
    result = subprocess.run(
        [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path,
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    try:
        return float(result.stdout.strip())
    except (ValueError, TypeError):
        return None

def build_heatmap():
    today = datetime.date.today()
    start = today - datetime.timedelta(days=364)
    start -= datetime.timedelta(days=start.weekday())  # bazar ertəsindən başlasın

    logs = {w.date: w.seconds for w in WatchLog.objects.filter(date__gte=start)}

    weeks = []
    current = start
    last_month = None
    while current <= today:
        week_days = []
        week_month = None
        for i in range(7):
            day = current + datetime.timedelta(days=i)
            if day > today:
                week_days.append(None)
                continue
            seconds = logs.get(day, 0)
            if seconds <= 0:
                level = 0
            elif seconds < GOAL_SECONDS:
                level = 1
            elif seconds < GOAL_SECONDS * 2:
                level = 2
            elif seconds < GOAL_SECONDS * 3:
                level = 3
            else:
                level = 4
            week_days.append({
                'date': day,
                'minutes': int(seconds // 60),
                'level': level,
            })
            if day.day == 1:
                week_month = day.strftime('%b').lower()

        label = ''
        if week_month and week_month != last_month:
            label = week_month
            last_month = week_month

        weeks.append({'label': label, 'days': week_days})
        current += datetime.timedelta(days=7)
    return weeks

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.save()

            if video.subtitle and video.subtitle.name.lower().endswith('.srt'):
                srt_bytes = video.subtitle.read()
                srt_text = srt_bytes.decode('utf-8', errors='ignore')
                vtt_text = srt_to_vtt(srt_text)
                base_name = os.path.splitext(os.path.basename(video.subtitle.name))[0]
                video.subtitle.delete(save=False)
                video.subtitle.save(f"{base_name}.vtt", ContentFile(vtt_text.encode('utf-8')), save=True)

            duration = get_video_duration(video.file.path)
            if duration:
                video.duration = duration
                video.save()

            generate_thumbnail(video)

            return redirect('library:video_list')
    else:
        form = VideoUploadForm()
    return render(request, 'library/upload.html', {'form': form})


def video_list(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    heatmap = build_heatmap()
    return render(request, 'library/video_list.html', {'videos': videos, 'heatmap': heatmap})


def video_player(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = VideoNoteForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
    else:
        form = VideoNoteForm(instance=video)
    return render(request, 'library/player.html', {'video': video, 'note_form': form})


@csrf_exempt
def save_position(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        position = request.POST.get('position')
        duration = request.POST.get('duration')
        watched = request.POST.get('watched_seconds')

        if position is not None:
            video.last_position = float(position)
        if duration:
            video.duration = float(duration)
        video.save()

        if watched:
            try:
                watched_val = float(watched)
            except ValueError:
                watched_val = 0
            if watched_val > 0:
                today = datetime.date.today()
                log, _ = WatchLog.objects.get_or_create(date=today, defaults={'seconds': 0})
                log.seconds += watched_val
                log.save()

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)


@require_POST
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.file.delete(save=False)
    if video.thumbnail:
        video.thumbnail.delete(save=False)
    if video.subtitle:
        video.subtitle.delete(save=False)
    video.delete()
    return redirect('library:video_list')