from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import *
from .instaapi.InstagramAPI import InstagramAPI as API
from .instafuncs import IGFuncs,idtouser
import os
from random import randint
import json,requests


username,passw = "xtweetsx_1", "omar2003"
def get_id(username):
	url = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+username+"&rank_token=0.3953592318270893&count=1"
	response = requests.get(url)
	respJSON = response.json()
	try:
		user_id = str( respJSON['users'][0].get("user").get("pk") )
		return user_id
	except:
		return "Unexpected error"

"""
tweet = User.objects.get(username='xtweetsx_1')
account = Account.objects.filter(user=tweet)

account = account[len(account)-1] # Last Query

accountfollowers = (account.followers_list).strip('][').split(',')
accountunfollowers = (account.unfollowed_you_list).strip('][]').split(',')
print(accountunfollowers)
ac = accountfollowers
c = 0
aclist = []

accountunfollowerslist = [x.lstrip().replace('""','') for x in accountunfollowers]
print(accountunfollowerslist)
for i in ac:
    if c ==0:
        #pk = i.strip("}{''pk:")
        pk = i.replace("{'pk': ","")
        pk = int(pk.strip())
        aclist.append(pk)
        #print(pk)
        c+=1
    elif c==1:
        #username = i.replace("'username': '","")
        #username = username.strip("'").lstrip()
        #tempdict['username'] =username
        c+=1
    elif c==2:
        #private = i.replace("'private': ","")
        #private = private.replace('}',"").lstrip()

        c = 0
#print(aclist)

api = API('xtweetsx_1','omar2003')
api.login()

user = api.getUsernameInfo('3022959521')
#print(user,user,user.text)
currentfollowers = api.getTotalFollowers(api.username_id)

currentfollowerslist = []
for i in currentfollowers:
    follower =i['pk']
    currentfollowerslist.append(follower)

unfollowed_you_list = [x for x in aclist if not x in currentfollowerslist]
unfollowed_you_list_last = accountunfollowerslist + unfollowed_you_list
print(unfollowed_you_list_last)

tweet = User.objects.get(username='xtweetsx_1')
account = Account.objects.filter(user=tweet)

account = account[len(account)-1] # Last Query

adb = (account.dont_follow_you_back_list).strip('][]').split(',')
c = 0
aclist = []
cc = 0
for i in adb:
    if c ==0:
        pk = i.lstrip()

        pk = i.replace("{'pk': ","")
        pk = pk.strip()
        print(pk)
        c+=1
    elif c==1:
        username = i.replace("'username': '","")
        username = username.strip("'").lstrip()
        aclist.append(username)
        c+=1
    elif c==2:
        private = i.replace("'private': ","")
        private = private.replace('}',"").lstrip()
        c = 0
print(aclist)
print(currentfollowers)
===============================
bot = API("xtweetsx_1", "omar2003")
bot.login()
bot_id = bot.username_id


followers_tree = {}
followings_tree = {}
#followers = bot.getTotalFollowers(bot_id)
following = bot.getTotalFollowings(bot_id)

for i in following:
    id = i['pk']
    subfollowers = bot.getTotalFollowings(id)
    subfollowers = [i['pk'] for i in subfollowers ]
    print(subfollowers)
    followers_tree[id] = subfollowers
print(followers_tree)


bot = API("xtweetsx_1", "omar2003")
bot.login()
bot_id = bot.username_id

feed = bot.getTotalUserFeed(get_id('ahmedezzatpy'))
#id = feed[0]['pk']
feed = [post['pk'] for post in feed ]
likers_list = []
for post in feed :
    bot.getMediaLikers(post)
    likers = bot.LastJson['users']
    for liker in likers:
        likers_list.append(liker['username'])


r = {}
for i in likers_list:

   if i in r:
     r[i] = r[i]+1
   else:
     r[i] = 1

r_sorted_keys = sorted(r, key=r.get, reverse=True)

print(r.values())

		followers = (i.followers_list).strip('][').split(',')
		ac = accountfollowers
		c = 0
		aclist = []
		for i in ac:
			if c ==0:
				pk = i.replace("{'pk': ","")
				pk = int(pk.strip())
				aclist.append(pk)
				c+=1

			elif c==1:
				c+=1

			elif c==2:
				c = 0
"""
#igacc = IGFuncs("xtweetsx_1","omar2003")

def check_user(username):
	usernamenoid = username
	userid = get_id(username)

	accounts = Account.objects.all()
	checked_list = []
	found = False
	for i in accounts:
		if i.user not in checked_list:
			following = i.following_list

			if userid in following:

				user, passw = str(i.user), i.password
				found = True
				break

			else:
				checked_list.append(i.user)
	if found:
		bot = API(user,str(passw))
		bot.login()
		feed = bot.getTotalUserFeed(userid)
		USER = PrivateUncoveredacc.objects.get(username='ahmedezzatpy')
		photo_name = 8721374422
		for i in feed:
			try:
				img_url = i['image_versions2']['candidates'][0]['url']
			except:
				img_url = i['carousel_media'][0]['image_versions2']['candidates'][0]['url']
			photo_name += 1
			imglink = str(USER)+"/"+str(photo_name)+".jpg"
			imgcreatelink = "media"+"/"+str(USER)+"/"+str(photo_name)+".jpg"
			requests_url = requests.get(img_url)
			try:
				os.mkdir("media/"+str(USER))
			except:
				pass
			f = open(imgcreatelink, 'ab')
			f.write(requests_url.content)
			f.close()

			archive = PhotosArchive.objects.create(username=usernamenoid, img_link=img_url)
			archive.save()
			uncoveredphoto = PrivateUncoveredPhoto.objects.create(user=USER, img=imglink)
			uncoveredphoto.save()
check_user("joe_hesham_")
