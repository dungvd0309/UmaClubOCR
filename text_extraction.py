def clean_text(t):
    t = t.replace('Nlembers', 'Members').replace("Total Fans", "TotalFans")
    return t

def extract_member_from_text(lines):
    members = []
    current_member = []
    i = 0

    while i < len(lines):
        lines[i] = clean_text(lines[i])
        current_member = {'name': '', 'fans': ''}

        if "Members" in lines[i] or "Leader" in lines[i]:
            i += 1
            # Tên member từ sau "Members"/"Leader" đến trước "TotalFans"
            while i < len(lines) and 'TotalFans' not in lines[i]:
                current_member['name'] += clean_text(lines[i]) + ' '
                i += 1
            if not i < len(lines):
                current_member
                break
            current_member['name'] = current_member['name'].strip()
            # Số fans đằng sau "TotalFans"
            if "TotalFans" in lines[i]:
                i += 1
                current_member['fans'] = clean_text(lines[i]).replace(',', '').replace('.', '') # Loại bỏ dấu
                members.append(current_member)
        else:
            i += 1
    return members