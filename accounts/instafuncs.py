from .instaapi.InstagramAPI import InstagramAPI as API
import requests,json,re,hashlib

authtokens = tuple()


def checkTokens():
    if not authtokens:
        getTokens()


def getTokens():
    r = requests.get('https://instagram.com/', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0', }).text
    rhx_gis = json.loads(re.compile('window._sharedData = ({.*?});', re.DOTALL).search(r).group(1))['nonce']

    ppc = re.search(r'ProfilePageContainer.js/(.*?).js', r).group(1)
    r = requests.get('https://www.instagram.com/static/bundles/es6/ProfilePageContainer.js/' + ppc + '.js').text
    query_hash = re.findall(r'{value:!0}\);(?:var|const|let) .=\"([0-9a-f]{32})\"', r)[0]
    print(query_hash)

    global authtokens
    authtokens = tuple((rhx_gis, query_hash))
def const_gis(query):
    checkTokens()
    t = authtokens[0] + ':' + query
    x_instagram_gis = hashlib.md5(t.encode("utf-8")).hexdigest()
    return x_instagram_gis



def idtouser(userid):
    checkTokens()
    query_variable = '{"user_id":"' + str(userid) + '","include_reel":true}'
    header = {'X-Instagram-GIS': const_gis(query_variable),
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
              'X-Requested-With': 'XMLHttpRequest'}
    r = requests.get(
        'https://www.instagram.com/graphql/query/?query_hash=' + authtokens[1] + '&variables=' + query_variable,
        headers=header).text
    if json.loads(r).get("message") == 'rate limited':
        print('[x] Rate limit reached!\n[#] Unchecked ID: {}\n[!] Try again in a few minutes..\n'.format(userid))
        exit()
    try:
        username = json.loads(r)['data']['user']['reel']['user']['username']
        return username
    except:
        return "Error Retrieving the Account"




class IGFuncs():
    def __init__(self,user,password):
        self.igaccount = API(user,password)
        self.igaccount.login()
        user_id = self.igaccount.username_id
        followers = self.igaccount.getTotalFollowers(user_id)
        following = self.igaccount.getTotalFollowings(user_id)

        self.followers = len(followers)
        self.following = len(following)

        self.followerslist = []
        for i in followers:
            follower = dict(pk=i['pk'],username=i['username'],profile_pic_url=i['profile_pic_url'])
            self.followerslist.append(follower)

        self.followinglist = []
        for i in following:
            follower = dict(pk=i['pk'],username=i['username'],profile_pic_url=i['profile_pic_url'])
            self.followinglist.append(follower)

        self.mutuallist = [x for x in self.followinglist if x in self.followerslist]
        self.dontfollowyoubacklist = [x for x in self.followinglist if x not in self.followerslist]
        self.youdontfollowbacklist = [x for x in self.followerslist if x not in self.followinglist]

        self.mutual = len(self.mutuallist)
        self.dontfollowyouback = len(self.dontfollowyoubacklist)
        self.youdontfollowback = len(self.youdontfollowbacklist)

    def unfollowp(self,id):
        self.igaccount.unfollow(id)
if __name__ == '__main__':
    acc = IGFuncs('xtweetsx_1','omar2003')
