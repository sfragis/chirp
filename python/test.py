# export PYTHONPATH=/path/to/requests/dir

import requests
import unittest

base_url = "http://chirp-fabiostrozzi.rhcloud.com/api/"

class ChirpRestClientTest(unittest.TestCase):

    def test_people(self):
        '''
        Tests the /api/{user}/people REST interface.
        Checks the number of followed people and followers.
        '''
        r = requests.get(base_url + 'hulk.hogan' + '/people', headers={'Chirp-Token' : '54dd989c-60fe-11e2-a0f3-544249f16afb'})
        self.assertEquals(200, r.status_code, "Expected the 200 HTTP code")
        j = r.json()
        self.assertEquals(0, len(j[u'followed']), "Hulk Hogan follows nobody")
        self.assertEquals(2, len(j[u'followers']), "Hulk Hogan has two followers")

    def test_chirps(self):
        '''
        Tests the /api/{user}/chirps REST interface.
        Checks the number of returned posts.
        '''
        r = requests.get(base_url + 'fabio.strozzi' + '/chirps', headers={'Chirp-Token' : 'fc57c1fc-60fd-11e2-8d5b-544249f16afb'})
        self.assertEquals(200, r.status_code, "Expected the 200 HTTP code")
        j = r.json()
        self.assertEquals(17, len(j), "17 posts considering Fabio's and his followers'")
        mine = [p for p in j if p[u'user'][u'username'] == 'fabio.strozzi']
        self.assertEquals(4, len(mine), "I just have 4 chirps")
        theirs = [p for p in j if p[u'user'][u'username'] == 'jack.sparrow']
        self.assertEquals(4, len(theirs), "4 chirps are from Jack")
        theirs = [p for p in j if p[u'user'][u'username'] == 'ip.man']
        self.assertEquals(6, len(theirs), "6 chirps are from Ip Man")
        theirs = [p for p in j if p[u'user'][u'username'] == 'tiger.man']
        self.assertEquals(3, len(theirs), "3 chirps are from Tiger")

    def test_chirps(self):
        '''
        Tests the /api/{user}/chirps REST interface.
        Checks the number of returned posts when using a filtering keyword.
        '''
        r = requests.get(base_url + 'fabio.strozzi' + '/chirps', params={'search':'bOaT'}, headers={'Chirp-Token' : 'fc57c1fc-60fd-11e2-8d5b-544249f16afb'})
        self.assertEquals(200, r.status_code, "Expected the 200 HTTP code")
        j = r.json()
        self.assertEquals(2, len(j), "Just two posts contain the 'boat' word")

    def test_unathorized(self):
        r = requests.get(base_url + 'fabio.strozzi' + '/chirps')
        self.assertEquals(401, r.status_code, "Expected the 401 HTTP code")
        r = requests.get(base_url + 'fabio.strozzi' + '/people')
        self.assertEquals(401, r.status_code, "Expected the 401 HTTP code")
        r = requests.get(base_url + 'fabio.strozzi' + '/chirps?search=anything')
        self.assertEquals(401, r.status_code, "Expected the 401 HTTP code")
        r = requests.put(base_url + 'fabio.strozzi' + '/follow')
        self.assertEquals(401, r.status_code, "Expected the 401 HTTP code")
        r = requests.put(base_url + 'fabio.strozzi' + '/unfollow')
        self.assertEquals(401, r.status_code, "Expected the 401 HTTP code")

    def test_invalid_token(self):
        r = requests.get(base_url + 'hulk.hogan' + '/people', headers={'Chirp-Token' : '1111-1111-1111-1111'})
        self.assertEquals(401, r.status_code, "Expected the 401 HTTP code")

    def test_not_found(self):
        # token must be valid in this case, otherwise the 401 will be returned
        r = requests.get(base_url + 'batman' + '/people', headers={'Chirp-Token' : 'fc57c1fc-60fd-11e2-8d5b-544249f16afb'})
        self.assertEquals(404, r.status_code, "Expected the 404 HTTP code")

    def test_follow_unfollow(self):
        # lets see how many person ip.man is following
        r = requests.get(base_url + 'ip.man' + '/people', headers={'Chirp-Token' : '54dd989c-60fe-11e2-a0f3-544249f16afb'})
        self.assertEquals(200, r.status_code, "Expected the 200 HTTP code")
        j = r.json()
        followed_by_ip_man = len(j[u'followed'])

        # here we have ip.man (identified by 54dd989c-60fe-11e2-a0f3-544249f16afb) starting to follow jack sparrow
        r = requests.put(base_url + 'jack.sparrow' + '/follow', headers={'Chirp-Token' : '54dd989c-60fe-11e2-a0f3-544249f16afb'})
        self.assertEquals(200, r.status_code, "Expected the 200 HTTP code")
        j = r.json()
        self.assertEquals(True, j, "Successfully following Jack Sparrow from now on")

        # counting followed people again
        r = requests.get(base_url + 'ip.man' + '/people', headers={'Chirp-Token' : '54dd989c-60fe-11e2-a0f3-544249f16afb'})
        self.assertEquals(200, r.status_code, "Expected the 200 HTTP code")
        j = r.json()
        self.assertEquals(followed_by_ip_man + 1, len(j[u'followed']), "Following one more person")

        # now stop following jack
        r = requests.put(base_url + 'jack.sparrow' + '/unfollow', headers={'Chirp-Token' : '54dd989c-60fe-11e2-a0f3-544249f16afb'})
        self.assertEquals(200, r.status_code, "Expected the 200 HTTP code")
        j = r.json()
        self.assertEquals(True, j, "Time to stop following Jack Sparrow")

        # counting followed people again
        r = requests.get(base_url + 'ip.man' + '/people', headers={'Chirp-Token' : '54dd989c-60fe-11e2-a0f3-544249f16afb'})
        self.assertEquals(200, r.status_code, "Expected the 200 HTTP code")
        j = r.json()
        self.assertEquals(followed_by_ip_man, len(j[u'followed']), "Following the initial amount of people")

if __name__ == '__main__':
    unittest.main()