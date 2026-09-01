import os
import json
from tinytag import TinyTag

audio_dir = 'audio'
covers_dir = 'covers'
lyrics_dir = 'lyrics'
playlist = []

# Quét tất cả các file trong thư mục audio
for filename in os.listdir(audio_dir):
    if filename.endswith('.mp3'):
        filepath = os.path.join(audio_dir, filename)
        
        # Đọc metadata từ file mp3
        tag = TinyTag.get(filepath)
        
        base_name = filename[:-4]
        
        # Trích xuất các thông tin cơ bản, có fallback nếu bị trống
        title = tag.title if tag.title else base_name
        artist = tag.artist if tag.artist else "Unknown Artist"
        album = tag.album if tag.album else "Unknown Album"
        
        # Tạo ID cơ bản
        song_id = base_name.replace(" ", "_").lower()
        
        # Xử lý tên Cover theo format "Cover-TênAlbum.jpg"
        cover_filename = f"Cover-{album}.jpg"
        cover_path = f"{covers_dir}/{cover_filename}"
        
        # Nếu ảnh .jpg không tồn tại, thử tìm .png, nếu vẫn không có thì để trống
        if not os.path.exists(cover_path):
            if os.path.exists(f"{covers_dir}/Cover-{album}.png"):
                cover_path = f"{covers_dir}/Cover-{album}.png"
            else:
                cover_path = "" # Hoặc thay bằng đường dẫn ảnh mặc định của bạn
                
        # Xử lý Lyrics: Chỉ lấy đường dẫn nếu file .lrc thực sự tồn tại trong thư mục
        lyric_path = f"{lyrics_dir}/{base_name}.lrc"
        has_lyric = os.path.exists(lyric_path)

        # Đóng gói dữ liệu bài hát
        song_info = {
            "id": song_id,
            "name": title,
            "artist": artist,
            "album": album,
            "audio": f"{audio_dir}/{filename}",
            "cover": cover_path,
            # Các thông tin metadata mở rộng
            "duration": round(tag.duration) if tag.duration else 0,
            "track": tag.track,
            "disc": tag.disc,
            "album_artist": tag.albumartist,
            "year": tag.year,
            "genre": tag.genre
        }
        
        # Chỉ chèn key "lyric" vào JSON nếu tìm thấy file
        if has_lyric:
            song_info["lyric"] = lyric_path

        playlist.append(song_info)

# Xuất ra file playlist.json
with open('playlist.json', 'w', encoding='utf-8') as f:
    json.dump(playlist, f, ensure_ascii=False, indent=2)

print(f"Đã tạo playlist.json thành công với {len(playlist)} bài hát!")