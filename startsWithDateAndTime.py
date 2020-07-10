import re
def startsWithDateAndTime(s):
    # regex pattern for date.(Works only for android. IOS Whatsapp export format is different. Will update the code soon
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9][0-9][0-9][0-9]), ([0-9]+):([0-9][0-9]) -'
    result = re.match(pattern, s)
    if result:
        return True
    return False
