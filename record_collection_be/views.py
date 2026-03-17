import requests as http_requests
from django.db.models import ProtectedError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Artist, Song, Album

DISCOGS_BASE = 'https://api.discogs.com'


def _discogs_headers():
    import os
    headers = {'User-Agent': 'RecordCollection/1.0'}
    token = os.environ.get('DISCOGS_TOKEN')
    if token:
        headers['Authorization'] = f'Discogs token={token}'
    return headers


class ArtistList(generics.ListCreateAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        return Artist.objects.filter(user_id=self.request.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user_id)


class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArtistSerializer

    def get_queryset(self):
        return Artist.objects.filter(user_id=self.request.user_id)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'detail': 'This artist has albums. Remove their albums before deleting.'},
                status=status.HTTP_409_CONFLICT
            )


class AlbumList(generics.ListCreateAPIView):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(user_id=self.request.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user_id)


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(user_id=self.request.user_id)


class SongList(generics.ListCreateAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.filter(album__user_id=self.request.user_id)


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.filter(album__user_id=self.request.user_id)


class DiscogsSearch(generics.GenericAPIView):
    def get(self, request):
        import re
        q = request.GET.get('q', '').strip()
        if not q:
            return Response({'results': []})
        search_type = request.GET.get('type', 'master')
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', q)
        clean_q = re.sub(r'\b(19\d{2}|20\d{2})\b', '', q).strip() if year_match else q
        use_year = year_match and len(clean_q) > 0
        is_catno = bool(re.match(r'^[A-Za-z0-9][-A-Za-z0-9]+$', q) and re.search(r'[A-Za-z]', q) and re.search(r'\d', q))
        params = {
            'type': search_type,
            'per_page': 10,
        }
        if is_catno:
            params['catno'] = q
        else:
            params['q'] = clean_q if use_year else q
            if use_year:
                params['year'] = year_match.group(0)
        try:
            resp = http_requests.get(
                f'{DISCOGS_BASE}/database/search',
                params=params,
                headers=_discogs_headers(),
                timeout=5,
            )
            return Response(resp.json())
        except Exception:
            return Response({'results': []}, status=502)


class DiscogsRelease(generics.GenericAPIView):
    def get(self, request, release_id):
        try:
            resp = http_requests.get(
                f'{DISCOGS_BASE}/releases/{release_id}',
                headers=_discogs_headers(),
                timeout=5,
            )
            return Response(resp.json())
        except Exception:
            return Response({}, status=502)


class DiscogsMaster(generics.GenericAPIView):
    def get(self, request, master_id):
        try:
            resp = http_requests.get(
                f'{DISCOGS_BASE}/masters/{master_id}',
                headers=_discogs_headers(),
                timeout=5,
            )
            data = resp.json()
            main_release_id = data.get('main_release')
            if main_release_id and not data.get('labels'):
                release_resp = http_requests.get(
                    f'{DISCOGS_BASE}/releases/{main_release_id}',
                    headers=_discogs_headers(),
                    timeout=5,
                )
                release_data = release_resp.json()
                data['labels'] = release_data.get('labels', [])
                if not data.get('released') and release_data.get('released'):
                    data['released'] = release_data['released']
            return Response(data)
        except Exception:
            return Response({}, status=502)


class DiscogsImage(generics.GenericAPIView):
    def get(self, request):
        from django.http import HttpResponse
        url = request.GET.get('url', '')
        if not url or 'discogs.com' not in url:
            return HttpResponse(status=400)
        try:
            resp = http_requests.get(url, headers=_discogs_headers(), timeout=5)
            return HttpResponse(
                resp.content,
                content_type=resp.headers.get('content-type', 'image/jpeg')
            )
        except Exception:
            return HttpResponse(status=502)
