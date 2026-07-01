import os, sys
os.chdir(r'k:\FitnessSystem\后端\admin_project')
sys.path.insert(0, r'k:\FitnessSystem\后端\admin_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_project.settings')
import django; django.setup()

# Simulate the frames endpoint with annotation ID 6
from fitness.models import AnnotatedVideo, AnnotatedFrame
import json

annotation_id = 6
start_frame = 0
end_frame = 150

try:
    annotation = AnnotatedVideo.objects.get(id=annotation_id)
    queryset = AnnotatedFrame.objects.filter(video=annotation).order_by('frame_index')
    queryset = queryset.filter(frame_index__gte=start_frame)
    if end_frame:
        queryset = queryset.filter(frame_index__lte=int(end_frame))
    frames = []
    for f in queryset[:5]:
        frames.append({
            'frame_index': f.frame_index,
            'timestamp': f.timestamp,
            'landmarks': json.loads(f.landmarks),
            'is_valid': f.is_valid,
        })
    print(f"API would return: code=200, {len(frames)} frames")
    print(f"First frame: index={frames[0]['frame_index']}, is_valid={frames[0]['is_valid']}, lm_len={len(frames[0]['landmarks'])}")
    print(f"Last frame: index={frames[-1]['frame_index']}")
    # What lastFetchedRange would be set to
    print(f"lastFetchedRange would be: start={start_frame}, end={end_frame}")
    # Check if annotation 6 is complete
    print(f"Annotation 6 status: {annotation.status}")
except Exception as e:
    print(f"Error: {e}")
