#!/usr/bin/env python3
"""
视频处理和文字提取
支持音频提取、ASR 转文字、字幕提取
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, List


class VideoProcessor:
    """视频处理器"""

    def __init__(self, asr_engine: str = "whisper"):
        """
        初始化视频处理器

        Args:
            asr_engine: ASR 引擎类型（whisper, faster-whisper）
        """
        self.asr_engine = asr_engine
        self.temp_dir = tempfile.mkdtemp()

    def extract_text(self, video_path: str, method: str = "auto") -> str:
        """
        从视频中提取文字

        Args:
            video_path: 视频本地路径或 URL
            method: 提取方法（asr, subtitle, auto）

        Returns:
            提取的文字内容
        """
        local_path = video_path

        if video_path.startswith(('http://', 'https://')):
            local_path = self._download_video(video_path)

        try:
            if method == "auto":
                text = self._extract_with_auto_method(local_path)
            elif method == "subtitle":
                text = self._extract_subtitles(local_path)
            elif method == "asr":
                text = self._extract_with_asr(local_path)
            else:
                raise ValueError(f"不支持的提取方法: {method}")

            return text
        finally:
            if local_path != video_path:
                self._cleanup_file(local_path)

    def _extract_with_auto_method(self, video_path: str) -> str:
        """自动选择最佳方法提取文字"""
        subtitle_text = self._extract_subtitles(video_path)
        if subtitle_text.strip():
            return subtitle_text

        return self._extract_with_asr(video_path)

    def _extract_subtitles(self, video_path: str) -> str:
        """提取视频内嵌字幕"""
        import pysrt

        temp_srt = os.path.join(self.temp_dir, "temp.srt")

        try:
            subprocess.run(
                ['ffmpeg', '-i', video_path, '-map', '0:s:0', temp_srt],
                capture_output=True,
                timeout=300
            )

            if os.path.exists(temp_srt):
                subs = pysrt.open(temp_srt)
                texts = [sub.text for sub in subs]
                return "\n".join(texts)

            return ""
        except (subprocess.CalledProcessError, FileNotFoundError, Exception):
            return ""
        finally:
            if os.path.exists(temp_srt):
                os.unlink(temp_srt)

    def _extract_with_asr(self, video_path: str) -> str:
        """使用 ASR 引擎提取音频转文字"""
        audio_path = self._extract_audio(video_path)

        try:
            if self.asr_engine == "whisper":
                return self._transcribe_with_whisper(audio_path)
            elif self.asr_engine == "faster-whisper":
                return self._transcribe_with_faster_whisper(audio_path)
            else:
                raise ValueError(f"不支持的 ASR 引擎: {self.asr_engine}")
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)

    def _extract_audio(self, video_path: str) -> str:
        """从视频中提取音频"""
        audio_path = os.path.join(self.temp_dir, "audio.wav")

        subprocess.run(
            ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le',
             '-ar', '16000', '-ac', '1', audio_path],
            capture_output=True,
            timeout=600
        )

        return audio_path

    def _transcribe_with_whisper(self, audio_path: str) -> str:
        """使用 Whisper 转录音频"""
        try:
            import whisper
        except ImportError:
            raise ImportError(
                "Whisper 未安装。请运行: pip install openai-whisper"
            )

        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="zh")
        return result["text"].strip()

    def _transcribe_with_faster_whisper(self, audio_path: str) -> str:
        """使用 Faster-Whisper 转录音频"""
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            raise ImportError(
                "Faster-Whisper 未安装。请运行: pip install faster-whisper"
            )

        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_path, language="zh")

        texts = [segment.text for segment in segments]
        return "".join(texts).strip()

    def _download_video(self, url: str) -> str:
        """下载视频到临时文件"""
        try:
            import yt_dlp
        except ImportError:
            raise ImportError(
                "yt-dlp 未安装。请运行: pip install yt-dlp"
            )

        output_path = os.path.join(self.temp_dir, "video.%(ext)s")

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

    def _cleanup_file(self, path: str):
        """清理临时文件"""
        try:
            if os.path.isfile(path):
                os.unlink(path)
        except Exception:
            pass

    def __del__(self):
        """清理临时目录"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception:
            pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python video_processor.py <video_path_or_url> [method]")
        sys.exit(1)

    method = sys.argv[2] if len(sys.argv) > 2 else "auto"
    processor = VideoProcessor()
    text = processor.extract_text(sys.argv[1], method)
    print("提取的文字内容：")
    print(text)
