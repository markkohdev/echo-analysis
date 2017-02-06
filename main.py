import os
import facebook
import csv
import json
import string
import operator

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


    for fb_id, obj in sources.items():
        print('Fetching feed for {}...'.format(obj.get('name')))
        try:
            response = graph.get_object(fb_id, fields='feed,id')
            message_items = response.get('feed', {}).get('data', [])

            posts = []
            for item in message_items:
                item_detail = graph.get_object(item.get('id'), fields='id,link,message,shares')
                print(json.dumps(item_detail,indent=2))
                posts.append(item_detail)

            sources[fb_id]['posts'] = posts
        except facebook.GraphAPIError as e:
            print('Unable to get messages for {}({}): {}'.format(obj.get('name'), fb_id, e))

    blue_terms = {}
    red_terms = {}

    for fb_id, obj in sources.items():
        side = obj.get('side')
        messages = [post.get('message', '') for post in obj.get('posts',[])]

        # Merge all messages into one string and remove punctuation from them
        messages_concated = ' '.join(messages).split(' ')
        translation_map = str.maketrans('','',string.punctuation)
        messages_cleaned = messages_concated.translate(translation_map)

        for term in messages_cleaned:
            if side == 'left':
                blue_terms[term] = blue_terms.get(term, 0) + 1
            else:
                red_terms[term] = red_terms.get(term, 0) + 1

    # Determine terms common between the two sides and remove them from the dictionaries
    common_terms = set(blue_terms.keys()).intersection(red_terms.keys())
    for term in common_terms:
        del blue_terms[term]
        del red_terms[term]

    # Sort the dictionary into a list of tuples by value
    blue_sorted = sorted(blue_terms.items(), key=operator.itemgetter(1), reverse=True)
    red_sorted = sorted(red_terms.items(), key=operator.itemgetter(1), reverse=True)

    print_header('Liberal Terms')
    print(blue_sorted[:10])

    print_header('Conservative Terms')
    print(red_sorted[:10])


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
