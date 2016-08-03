import requests


class Emailer(object):
    '''Sends email through mailgun.'''

    def __init__(self, domain, api_key,
                 api_url="https://api.mailgun.net/v3/{}/messages"):
        self.domain = domain
        self.api_key = api_key
        self.api_url = api_url

    def send(self, from_, to_, subject, text='', html=''):
        if not all([from_, to_, subject, any([text, html])]):
            return None
        if isinstance(to_, basestring):
            to_ = [to_]
        return requests.post(
            self.api_url.format(self.domain),
            auth=("api", self.api_key),
            data={"from": from_,
                  "to": to_,
                  "subject": subject,
                  "text": text,
                  "html": html,
                  })
