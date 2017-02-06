import os
import facebook
import csv
import json
import string

################################################################################
# Main Demo Function
################################################################################

def main():
    """
    Our main function that will get run when the program executes
    """
    print_header('Data Hack Jawn', length=50)

    app_id = os.environ.get('FACEBOOK_APP_ID')
    app_secret = os.environ.get('FACEBOOK_APP_SECRET')

    access_token = facebook.GraphAPI().get_app_access_token(app_id, app_secret)

    graph = facebook.GraphAPI(access_token)

    sources = {}

    with open('red_blue_sources.csv') as infile:
        reader = csv.reader(infile)
        next(reader)
        for row in reader:
            fb_id = row[0]
            side = row[7]
            name = row[10]
            sources[fb_id] = {
                'name': name,
                'side': side,
            }

    translation_map = str.maketrans('','',string.punctuation)

    for fb_id, obj in sources.items():
        print(obj.get('name'))
        response = graph.get_object(fb_id, fields='feed')
        messages = [item.get('message') for item in response.get('feed', {}).get('data', []) if item.get('message')]
        print(messages)
        messages_cleaned = [message.translate(translation_map) for message in messages]

        sources[fb_id]['messages'] = messages_cleaned

        print(messages_cleaned)


################################################################################
# Convenience Functions
################################################################################

def print_header(message, length=30):
    """
    Given a message, print it with a buncha stars all header-like
    :param message: The message you want to print
    :param length: The number of stars you want to surround it
    """
    print('\n' + ('*' * length))
    print(message)
    print('*' * length)

################################################################################
# Authentication Functions
################################################################################


if __name__ == '__main__':
    main()
