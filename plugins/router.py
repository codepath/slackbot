from rtmbot.core import Plugin

def list_companies():
    print 'list companies'


def whos_hiring():
    print 'whos hiring'


def whos_hiring_at_company(company_name):
    print 'whos hiring at {}'.format(company_name)


def alumni_at_company(company_name):
    print 'alumni at {}'.format(company_name)


def match(template, text):
    # returns a tuple of (bool, dict) where the first value is
    # whether or not there was a match and the second value is
    # the data that was matched
    vars = {}
    template_tokens = template.split(' ')
    text_tokens = text.split(' ')

    if len(template_tokens) != len(text_tokens):
        return False, None

    for template_token, text_token in zip(template_tokens, text_tokens):
        if template_token.startswith('{'):
            key = template_token[1:-1]
            vars[key] = text_token
        elif template_token != text_token:
            return False, None

    return True, vars


class RoutingPlugin(Plugin):
    routes = {
        'list companies': list_companies,
        'alumni at {company_name}': alumni_at_company,
        'whos hiring at {company_name}': whos_hiring_at_company,
        'whos hiring': whos_hiring,
    }

    def process_message(self, data):
        # TODO: do we want to support edits? These come in as a diff format
        # TODO: some sort of warmup period to ignore initial messages in mailbox?
        print data
        text = data.get('text')
        if not text:
            return

        text = text.strip().lower()
        for trigger, func in self.routes.iteritems():
            matches, vars = match(trigger, text)
            if matches:
                func(**vars)
                break
        else:
            print 'i dont know what to do'
