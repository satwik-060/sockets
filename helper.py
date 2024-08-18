def log_reader_helper(file_path: str):
    lines_to_read = 5
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, 2)
            buffer = bytearray()
            pointer_location = f.tell()
            
            while pointer_location >= 0 and lines_to_read > 0:
                f.seek(pointer_location)
                pointer_location -= 1 
                new_byte = f.read(1)
                
                if new_byte == b'\n':
                    lines_to_read -= 1
                    if lines_to_read == 0:
                        break
                buffer.extend(new_byte)
            return buffer[::-1].decode('utf-8').splitlines()[-lines_to_read:]
    except Exception as exc:
        print(f"Error while reading log file: {exc}")
        return ""
