# def clean_text(t):
#     t = t.replace('Nlembers', 'Members')
#     return t

def extract_member_from_text(lines):
    members = []
    current_member = []
    i = 0

    while i < len(lines):
        # lines[i] = clean_text(lines[i])
        current_member = {'name': '', 'fans': ''}

        if "Members" in lines[i] or "Leader" in lines[i]:
            i += 1
            # Member name from after "Members"/"Leader" to before "TotalFans"
            while i < len(lines) and 'Total Fans' not in lines[i]:
                current_member['name'] += lines[i] + ' '
                i += 1
            if not i < len(lines):
                current_member
                break
            current_member['name'] = current_member['name'].strip()
            # Number of fans after "Total Fans"
            if "Total Fans" in lines[i]:
                i += 1
                current_member['fans'] = lines[i].replace(',', '').replace('.', '') # Remove punctuation
                members.append(current_member)
        else:
            i += 1
    return members
