from paddleocr import PaddleOCR

def init_ocr():
    """
    Initializes and returns a PaddleOCR instance
    """
    return PaddleOCR(use_angle_cls=True)

def ocr_to_lines(ocr, image):
    """
    Performs OCR on the given image and returns the recognized text lines.
    """
    result = ocr.predict(image)
    lines = result[0]['rec_texts']
    return lines

def extract_members_from_lines(lines):
    """
    Parses a list of text lines to extract club member names and their fan counts.
    """
    members = []
    current_member = []
    i = 0

    while i < len(lines):
        current_member = {'name': '', 'fans': ''}

        if "Members" in lines[i] or "Leader" in lines[i]:
            # Member name: from after "Members" or "Leader" to before "Total Fans"
            i += 1
            while i < len(lines) and 'Total Fans' not in lines[i]:
                current_member['name'] += lines[i] + ' '
                i += 1
            if not i < len(lines):
                current_member
                break
            current_member['name'] = current_member['name'].strip()

            # Number of fans: after "Total Fans"
            if "Total Fans" in lines[i]:
                i += 1
                current_member['fans'] = lines[i].replace(',', '').replace('.', '') # Remove punctuation
                members.append(current_member)
        else:
            i += 1
    return members