#!/usr/bin/env python

import json
from datetime import datetime
from os import environ as env
from os import path, sep
from sys import exit
from time import sleep

from slackclient import SlackClient

slack = SlackClient(env['SLACK_API_TOKEN'])

def error(message):
    print "error: {}".format(message)

def fatal(message):
    error(message)
    exit(1)

def identity(value):
    return value

def yes_no(value):
    if value:
        return value.lower() == 'yes'

def truthy(value):
    return bool(value)

custom_fields = {
    'current_company': ('Xf4XTG8KD0', identity),
    'current_position': ('Xf4XTGJ42E', identity),
    'linkedin_profile': ('Xf4Y0T487P', identity),
    'github_username': ('Xf3V0Z88F7', identity),
    'alumni_since_date': ('Xf4YJ6A54N', identity),
    'hiring_for': ('Xf4XTT5YRG', identity),
    'is_hiring': ('Xf4XTT5YRG', truthy),
    'is_mentor': ('Xf4XRMTE9H', yes_no),
}

def is_valid_user(user):
    restricted = user.get('is_restricted') or user.get('is_ultra_restricted')
    bot = user.get('is_bot')
    deleted = user.get('deleted')
    return not restricted and not bot and not deleted


def merged_profile(user, profile):
    result = {
        'first_name': profile.get('first_name') or '',
        'last_name': profile.get('last_name') or '',
        'slack_name': user['name'],
        'slack_id': user['id'],
        'email': profile.get('email'),
        'last_updated_profile_at': str(datetime.fromtimestamp(user['updated'])),
        'last_updated_record_at': str(datetime.now()),
    }

    fields = profile.get('fields') or {}
    for key, v in custom_fields.iteritems():
        result[key] = None
        field_id, transform = v

        data = fields.get(field_id)
        if data:
            result[key] = transform(data['value'])

    return result


def is_ok(result):
    return bool(result.get('ok'))

if __name__ == '__main__':
    result = slack.api_call('users.list')
    if not is_ok(result):
        fatal("failed to get list of users")

    profiles = []
    users = [u for u in result['members'] if is_valid_user(u)]

    for user in users:
        user_id = user['id']
        user_name = user['name']

        result = slack.api_call('users.profile.get', user=user_id)
        if not is_ok(result):
            error("failed to get user {} ({})".format(user_name, user_id))
            continue

        profile = merged_profile(user, result['profile'])
        profiles.append(profile)
        sleep(1)

    file_path = path.abspath(path.join(sep, env['SLACKBOT_BASE_PATH'], 'profile_data.json'))
    file_handle = open(file_path, 'w')
    if file_handle:
        file_handle.write(json.dumps(profiles))
        file_handle.close()
        print "Profile data saved to file"
    else:
        print "Invalid file handle"
