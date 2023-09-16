import shutil
import time

def move_file(source_paths, destination):
    success = 0
    failed = 0
    total_files = len(source_paths)
    animation_length = total_files * 20

    animation_frames = ["|", "/", "-", "\\"]
    
    for i, source in enumerate(source_paths, start=1):
        for _ in range(20):
            progress = int(((_ + (i - 1) * 20) / animation_length) * 100)
            animation_frame = animation_frames[(_ + (i - 1)) % len(animation_frames)]
            progress_bar = f"[{'#' * _}{'-' * (20 - _)}]"
            print(f"\rMoving: {progress_bar} {progress}% {animation_frame} ({i}/{total_files})", end="")
            time.sleep(0.1)  # Adjust the delay as needed
        
        try:
            shutil.move(source, destination)
        except FileNotFoundError:
            print(f"Err: ['{source}'] not found", "red")
            failed = failed + 1
        except Exception as e:
            print(f"Err: {e}", "red")
            failed = failed + 1
        else:
            success = success + 1
    
    print(f"Total files moved: {success + failed} | Success move: {success} | Failed move: {failed}", "green")