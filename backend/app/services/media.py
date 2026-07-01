import io
import struct
from PIL import Image

from app.exceptions import ImageResolutionExceededException


def process_image(file_data: bytes) -> bytes:
    image = Image.open(io.BytesIO(file_data))
    
    # Предотвращение Pixel Flood DoS
    width, height = image.size
    if width > 4096 or height > 4096:
        raise ImageResolutionExceededException()

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    out_bytes = io.BytesIO()
    image.save(out_bytes, format="WEBP", quality=80)
    return out_bytes.getvalue()


def get_mp4_duration(file_data: bytes) -> float:
    f = io.BytesIO(file_data)

    def read_boxes(stream, limit=None):
        boxes = {}
        bytes_read = 0
        while limit is None or bytes_read < limit:
            header = stream.read(8)
            if len(header) < 8:
                break
            bytes_read += 8
            size, box_type = struct.unpack(">I4s", header)
            box_type = box_type.decode("latin1", errors="ignore")

            if size < 8:
                break

            header_size = 8
            if size == 1:
                size_header = stream.read(8)
                bytes_read += 8
                size = struct.unpack(">Q", size_header)[0]
                if size < 16:
                    break
                header_size = 16

            data_size = size - header_size if size >= header_size else 0
            if box_type in ("moov", "trak", "mdia", "minf", "stbl"):
                nested = read_boxes(stream, limit=data_size)
                boxes[box_type] = nested
                bytes_read += data_size
            elif box_type == "mvhd":
                # mvhd содержит структуру фиксированного размера. Читаем максимум 128 байт,
                # чтобы избежать выделения гигабайтов памяти, если data_size фейковый.
                read_size = min(data_size, 128)
                mvhd_data = stream.read(read_size)
                bytes_read += read_size
                if data_size > read_size:
                    stream.seek(data_size - read_size, io.SEEK_CUR)
                    bytes_read += (data_size - read_size)

                if len(mvhd_data) >= 20:
                    version = mvhd_data[0]
                    if version == 1 and len(mvhd_data) >= 32:
                        timescale, duration = struct.unpack(">IQ", mvhd_data[20:32])
                        boxes["mvhd"] = (timescale, duration)
                    elif version != 1:
                        timescale, duration = struct.unpack(">II", mvhd_data[12:20])
                        boxes["mvhd"] = (timescale, duration)
            else:
                stream.seek(data_size, io.SEEK_CUR)
                bytes_read += data_size
        return boxes

    try:
        boxes = read_boxes(f)
        if "moov" in boxes and "mvhd" in boxes["moov"]:
            timescale, duration = boxes["moov"]["mvhd"]
            return float(duration) / float(timescale)
    except Exception:
        pass
    return 0.0
