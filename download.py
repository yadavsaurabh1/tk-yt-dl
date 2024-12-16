from time import sleep

import yt_dlp
from download_window import DownloadWindow

class Download:
    def __init__(self, URLS : list, master):
        self.URLS = URLS
        self.master = master

        self.download(URLS)

    def download(self, URLS : list):
        ydl_opts = {
            'format': self.format_selector,
            'progress_hooks': [self.progressBar]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(URLS)

    def progressBar(self, progress):
        print(progress)

    def format_selector(self, ctx):
        formats = {'video' : {}, 'audio' : {}}
        formatInfos = ctx.get('formats')
        
        for formatInfo in formatInfos:
            if formatInfo['video_ext'] != 'none' and formatInfo['audio_ext'] == 'none':
                if formatInfo['ext'] not in formats['video']: formats['video'][formatInfo['ext']] = {}
                formats['video'][formatInfo['ext']][formatInfo['resolution'].split('x')[-1] + 'p' + str(int(formatInfo['fps'])) + ' ' + formatInfo['dynamic_range']] = formatInfo['format_id']
            elif formatInfo['audio_ext'] != 'none' and formatInfo['video_ext'] == 'none':
                if formatInfo['ext'] not in formats['audio']: formats['audio'][formatInfo['ext']] = {}
                formats['audio'][formatInfo['ext']][formatInfo['format_note']] = formatInfo['format_id']

        choice = [None, None, False]
        downloadWindow = DownloadWindow(self.master, choice, formats)
        self.master.wait_window(downloadWindow)

        if choice[2] is not True: return

        audio = None
        video = None

        if choice[0] is not None:
            for formatInfo in formatInfos:
                if formatInfo['format_id'] == choice[0]: video = formatInfo

        if choice[1] is not None:
            for formatInfo in formatInfos:
                if formatInfo['format_id'] == choice[1]: audio = formatInfo

        if video is not None and audio is not None:
            yield {
                'format_id': f'{video["format_id"]}+{audio["format_id"]}',
                'ext': video['ext'],
                'requested_formats': [video, audio],
                'protocol': f'{video["protocol"]}+{audio["protocol"]}'
            }

        elif video is not None:
            yield {
                'format_id': f'{video["format_id"]}',
                'ext': video['ext'],
                'requested_formats': [video],
                'protocol': f'{video["protocol"]}'
            }

        elif audio is not None:
            yield {
                'format_id': f'{audio["format_id"]}',
                'ext': audio['ext'],
                'requested_formats': [audio],
                'protocol': f'{audio["protocol"]}'
            }