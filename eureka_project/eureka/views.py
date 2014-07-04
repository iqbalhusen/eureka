'''
Created on 18-May-2014

@author: iqbal
'''
import datetime
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from eureka.models import *
from eureka.forms import *
from django.db.models import Max, F, Q
from django.templatetags.static import static


def index(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_list = Category.objects.extra(
                                           select={'likes_n_views':'likes+views'},
                                           order_by=('-likes_n_views',)
                                           )[:5]
                                           
    context_dict = {'categories':category_list}
    top_article_list = Article.objects.exclude(views=0, likes=0).extra(select={'likes_n_views':'likes+views'},order_by=('-likes_n_views',))[:5]
    
    for article in top_article_list:
        category = Category.objects.get(id=int(article.category_id))
        category_url = encode(category.name)
        article.category_url = category_url
        article.category_name = category.name
        
    context_dict['top_article_list'] = top_article_list
    context_dict['cat_list'] = cat_list
    
    for category in category_list:
        category.url = encode(category.name)
    
    #Code for cookies
    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0) #http://stackoverflow.com/questions/12166368/django-request-session-getname-false-what-does-this-code-mean
        if (datetime.datetime.now() - datetime.datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.datetime.now())
    else:
        request.session['last_visit'] = str(datetime.datetime.now())
        request.session['visits'] = 1
        
    return render_to_response('eureka/index.html', context_dict, context)


def pub_profile(request, username):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list':cat_list}
    
    try:
        user = User.objects.get(username__iexact=username)
        user_profile = UserProfile.objects.get(user_id=int(user.id))
        context_dict['user_pub'] = user
        context_dict['user_profile'] = user_profile
    
    except User.DoesNotExist or UserProfile.DoesNotExist:
        pass
    
    return render_to_response('eureka/pub_profile.html', context_dict, context)


@login_required
def profile(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list':cat_list}
    u = User.objects.get(username=request.user)
    
    try:
        up = UserProfile.objects.get(user=u)
    except:
        up = None
        
    context_dict['user'] = u
    context_dict['user_profile'] = up
    
    return render_to_response('eureka/profile.html', context_dict, context)


def about(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {'cat_list':cat_list}
    
    return render_to_response('eureka/about.html', context_dict, context)


def category(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_name = decode(category_name_url)
    context_dict = {'category_name':category_name,'cat_list':cat_list,'category_name_url':category_name_url}
    
    try:
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
          
        article_list_latest = Article.objects.filter(isPublished=True, category=category.id).order_by('-publishedOn')[:5]
        article_list_popular = Article.objects.filter(isPublished=True, category=category.id).exclude(views=0, likes=0).extra(
                                                 select={'likes_n_views':'likes+views'},
                                                 order_by=('-likes_n_views',)
                                                 )[:5]
        context_dict['article_list_latest'] = article_list_latest
        context_dict['article_list_popular'] = article_list_popular
        
    except Category.DoesNotExist or Article.DoesNotExist:
        pass
    
    #Code for Like
    try:
        checkLikeCategory = LikeCategory.objects.get(user_id=int(request.user.id), category_id=int(category.id))
        isLiked = False
        if checkLikeCategory:
            isLiked = True
        context_dict['isLiked'] = isLiked
    
    except:
        pass
      
    return render_to_response('eureka/category.html',context_dict, context)


def popular(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_name = decode(category_name_url)
    context_dict = {'category_name':category_name,'cat_list':cat_list,'category_name_url':category_name_url}
    
    try:
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
            
        article_list_popular = Article.objects.filter(isPublished=True, category=category.id).exclude(views=0, likes=0).extra(
                                                 select={'likes_n_views':'likes+views'},
                                                 order_by=('-likes_n_views',)
                                                 )
        
        #pagination
        paginator = Paginator(article_list_popular, 5)
        page = request.GET.get('page')
        popular_articles = None
        
        try:
            popular_articles = paginator.page(page)
        except PageNotAnInteger:
            popular_articles = paginator.page(1)
        except EmptyPage:
            popular_articles = paginator.page(paginator.num_pages)
        
        context_dict['article_list_popular'] = popular_articles
        
    except Category.DoesNotExist or Article.DoesNotExist:
        pass
    
    #Code for Like
    try:
        checkLikeCategory = LikeCategory.objects.get(user_id=int(request.user.id), category_id=int(category.id))
        isLiked = False
        if checkLikeCategory:
            isLiked = True
        context_dict['isLiked'] = isLiked
    
    except:
        pass

    return render_to_response('eureka/popular.html',context_dict, context)


def current_issue(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_name = decode(category_name_url)
    context_dict = {'category_name':category_name,'cat_list':cat_list,'category_name_url':category_name_url}
    
    try:
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
        
        current_volume = Article.objects.filter(isPublished=True, category=category.id).aggregate(max_volume=Max('volume'))
        current_volume_num = current_volume['max_volume']
        article_list_current_volume = Article.objects.filter(isPublished=True, category=category.id, volume=current_volume_num)
        current_issue = article_list_current_volume.aggregate(max_issue=Max('issue'))
        current_issue_num = current_issue['max_issue']                                        
        article_list_current = Article.objects.filter(isPublished=True, category=category.id, volume=current_volume_num, issue=current_issue_num).order_by('-publishedOn')
        
        context_dict['current_volume'] = current_volume_num
        context_dict['current_issue'] = current_issue_num
        
        paginator = Paginator(article_list_current, 5)
        page = request.GET.get('page')
        current_articles = None
        
        try:
            current_articles = paginator.page(page)
        except PageNotAnInteger:
            current_articles = paginator.page(1)
        except EmptyPage:
            current_articles = paginator.page(paginator.num_pages)
        
        context_dict['article_list_current'] = current_articles
        
    except Category.DoesNotExist or Article.DoesNotExist:
        pass
    
    #Code for Like
    try:
        checkLikeCategory = LikeCategory.objects.get(user_id=int(request.user.id), category_id=int(category.id))
        isLiked = False
        if checkLikeCategory:
            isLiked = True
        context_dict['isLiked'] = isLiked
    
    except:
        pass
        
    return render_to_response('eureka/current_issue.html',context_dict, context)
    

def archive(request, category_name_url):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_name = decode(category_name_url)
    context_dict = {'category_name':category_name,'cat_list':cat_list,'category_name_url':category_name_url}
    
    try:
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
        
        current_volume = Article.objects.filter(isPublished=True, category=category.id).aggregate(max_volume=Max('volume'))
        current_volume_num = current_volume['max_volume']
        article_list_current_volume = Article.objects.filter(isPublished=True, category=category.id, volume=current_volume_num)
        current_issue = article_list_current_volume.aggregate(max_issue=Max('issue'))
        current_issue_num = current_issue['max_issue']                                        
        volume_list = []
        if current_volume_num:
            for x in reversed(range(1, current_volume_num)):
                volume_list.append(x)
        
        context_dict['current_volume'] = current_volume_num
        context_dict['volume_list'] = volume_list
        context_dict['current_issue'] = current_issue_num
        
    except Category.DoesNotExist or Article.DoesNotExist:
        pass
    
    #Code for Like
    try:
        checkLikeCategory = LikeCategory.objects.get(user_id=int(request.user.id), category_id=int(category.id))
        isLiked = False
        if checkLikeCategory:
            isLiked = True
        context_dict['isLiked'] = isLiked
    
    except:
        pass
        
    return render_to_response('eureka/archive.html',context_dict, context)


def archive_volume_issue(request, category_name_url, volume_num, issue_num):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_name = decode(category_name_url)
    context_dict = {'category_name':category_name,'cat_list':cat_list,'category_name_url':category_name_url}
    
    try:
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
        volume = volume_num
        issue = issue_num
        article_list = Article.objects.filter(isPublished=True, category=category.id, volume=volume, issue=issue).order_by('-publishedOn')
        context_dict['volume'] = volume
        context_dict['issue'] = issue
        
        paginator = Paginator(article_list, 5)
        page = request.GET.get('page')
        articles = None
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        
        context_dict['article_list'] = articles
        
    except Category.DoesNotExist or Article.DoesNotExist:
        pass
    
    #Code for Like
    try:
        checkLikeCategory = LikeCategory.objects.get(user_id=int(request.user.id), category_id=int(category.id))
        isLiked = False
        if checkLikeCategory:
            isLiked = True
        context_dict['isLiked'] = isLiked
    
    except:
        pass
        
    return render_to_response('eureka/archive_volume_issue.html',context_dict, context)


def article(request, category_name_url, article_num):
    context = RequestContext(request)
    cat_list = get_category_list()
    category_name = decode(category_name_url)
    context_dict = {'category_name':category_name,'cat_list':cat_list,'category_name_url':category_name_url}
    article_id = article_num
    
    try:
        category = Category.objects.get(name__iexact=category_name)
        context_dict['category'] = category
        article = Article.objects.get(id=article_id)
        context_dict['article'] = article
        author = User.objects.get(id=article.uploader_id)
        try:
            author_profile = UserProfile.objects.get(user_id=author.id)
        except:
            author_profile = None
            
        context_dict['author'] = author
        context_dict['author_profile'] = author_profile
        keyword_list = article.keywords.split(',')
        keywords = []
        for x in keyword_list:
            keywords.append(x.strip())
        context_dict['keywords'] = keywords
    except Category.DoesNotExist or Article.DoesNotExist:
        pass
    
    #Code for Like
    try:
        checkLikeArticle = LikeArticle.objects.get(user_id=int(request.user.id), article_id=int(article.id))
        isLiked = False
        if checkLikeArticle:
            isLiked = True
        context_dict['isLiked'] = isLiked
    
    except:
        pass
    
    return render_to_response('eureka/article.html', context_dict, context)
    
    
@login_required
def like_article(request):
    article_id = None
    user_id = None
    if request.method == 'GET':
        article_id = request.GET['article_id']
        user_id = request.GET['user_id']
        
    likes = 0
    if article_id:
        article = Article.objects.get(id=int(article_id))
        user = User.objects.get(id=int(user_id))
        if article and user:
            newtup = LikeArticle(user=user,article=article)
            newtup.save()            
            likes = article.likes + 1
            article.likes = likes
            article.save()
        
    return HttpResponse(likes)


@login_required
def unlike_article(request):
    article_id = None
    user_id = None
    if request.method == 'GET':
        article_id = request.GET['article_id']
        user_id = request.GET['user_id']
        
    likes = 0
    if article_id:
        article = Article.objects.get(id=int(article_id))
        user = User.objects.get(id=int(user_id))
        if article and user:
            deltup = LikeArticle.objects.get(user_id=int(user.id), article_id=int(article.id))
            deltup.delete()
            likes = article.likes - 1
            article.likes = likes
            article.save()
        
    return HttpResponse(likes)


def view_article(request):
    article_id = None
    if request.method == 'GET':
        article_id = request.GET['article_id']
        
    views = 0
    if article_id:
        article = Article.objects.get(id=int(article_id))
        if article:           
            views = article.views + 1
            article.views = views
            article.save()
        
    return HttpResponse(views)


def view_category(request):
    category_id = None
    if request.method == 'GET':
        category_id = request.GET['category_id']
        
    views = 0
    if category_id:
        category = Category.objects.get(id=int(category_id))
        if category:           
            views = category.views + 1
            category.views = views
            category.save()
        
    return HttpResponse(views)


@login_required
def submit_manuscript(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            formdata = form.cleaned_data
            newtup = Article(
                             category = formdata['category'],
                             title = formdata['title'],
                             uploader = request.user,
                             abstract = formdata['abstract'],
                             keywords = formdata['keywords'],
                             pdf = formdata['pdf'],
                             )
            newtup.save()
            return thank_you_submit_manuscript(request)
        else:
            print form.errors
    else:
        form = ArticleForm()
    context_dict['form'] = form
    
    return render_to_response('eureka/submit_manuscript.html',context_dict, context)


@login_required
def thank_you_submit_manuscript(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list
    
    return render_to_response('eureka/thank_you_submit_manuscript.html', context_dict, context)


def register(request):    
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    
    context_dict['user_form'] = user_form
    context_dict['profile_form']= profile_form
    context_dict['registered'] = registered
    
    return render_to_response('eureka/register.html',context_dict,context)

def search_article(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list
    
    if request.method == 'POST':
        try:
            search_key = request.POST['search_key'].strip()
            search_key_list = search_key.split()
            
            if search_key_list:
                try:
                    article_list = Article.objects.filter(Q(reduce(lambda x, y: x& y,[Q(title__icontains=word) for word in search_key_list])) | Q(reduce(lambda x, y: x& y,[Q(abstract__icontains=word) for word in search_key_list]))).extra(select={'likes_n_views':'likes+views'}, order_by=('-likes_n_views',))
                    if not article_list:
                        article_list = Article.objects.filter(Q(reduce(lambda x, y: x| y,[Q(title__icontains=word) for word in search_key_list])) | Q(reduce(lambda x, y: x| y,[Q(abstract__icontains=word) for word in search_key_list]))).extra(select={'likes_n_views':'likes+views'}, order_by=('-likes_n_views',))
                    #reduce(lambda x, y: x| y,[Q(title__icontains=word) for word in search_key_list]) is a fancy way to write Q(title__contains=search_key_list[0]) | Q(title__contains=search_key_list[1]) | ... | Q(title__contains=search_key_list[-1])      
                    
                    for article in article_list:
                        category = Category.objects.get(id=int(article.category_id))
                        category_url = encode(category.name)
                        article.category_url = category_url
                        article.category_name = category.name
                                
                    total_articles = len(article_list)
                    context_dict['total_articles'] = total_articles
                    context_dict['article_list'] = article_list
                
                except Article.DoesNotExist or Category.DoesNotExist:
                    pass
            
        except:
            adv_search_key = request.POST['adv_search_key'].strip()
            adv_search_key_list = adv_search_key.split()
            cat_name = request.POST['category'].strip()
            
            if adv_search_key_list and cat_name:
                
                try:
                    article_list_temp = Article.objects.filter(Q(reduce(lambda x, y: x& y,[Q(title__icontains=word) for word in adv_search_key_list])) | Q(reduce(lambda x, y: x& y,[Q(abstract__icontains=word) for word in adv_search_key_list]))).extra(select={'likes_n_views':'likes+views'}, order_by=('-likes_n_views',))
                    if not article_list_temp:
                        article_list_temp = Article.objects.filter(Q(reduce(lambda x, y: x| y,[Q(title__icontains=word) for word in adv_search_key_list])) | Q(reduce(lambda x, y: x| y,[Q(abstract__icontains=word) for word in adv_search_key_list]))).extra(select={'likes_n_views':'likes+views'}, order_by=('-likes_n_views',))
                    
                    category = Category.objects.get(name=cat_name)
                    article_list = article_list_temp.filter(category_id=int(category.id))
                        
                    cat_url = encode(category.name)
                    context_dict['cat_url'] = cat_url
                    total_articles = len(article_list)
                    context_dict['cat_name'] = category.name
                    context_dict['total_articles'] = total_articles
                    context_dict['adv_article_list'] = article_list
                except Article.DoesNotExist or Category.DoesNotExist:
                    pass
        
    return render_to_response('eureka/search_result.html', context_dict, context)


def user_login(request):
    context = RequestContext(request)
    cat_list = get_category_list()
    context_dict = {}
    context_dict['cat_list'] = cat_list
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/eureka/')
            else:
                context_dict['disabled_account'] = True
                return render_to_response('eureka/login.html', context_dict, context)
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('eureka/login.html', context_dict, context)
    else:
        return render_to_response('eureka/login.html', context_dict, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/eureka')


@login_required
def like_category(request):
    cat_id = None
    user_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        user_id = request.GET['user_id']
        
    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        user = User.objects.get(id=int(user_id))
        if category and user:
            newtup = LikeCategory(user=user,category=category)
            newtup.save()
            
            likes = category.likes + 1
            category.likes = likes
            category.save()
        
    return HttpResponse(likes)


@login_required
def unlike_category(request):
    cat_id = None
    user_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']
        user_id = request.GET['user_id']
        
    likes = 0
    if cat_id:
        category = Category.objects.get(id=int(cat_id))
        user = User.objects.get(id=int(user_id))
        if category and user:
            deltup = LikeCategory.objects.get(user_id=int(user.id), category_id=int(category.id))
            deltup.delete()
            
            likes = category.likes - 1
            category.likes = likes
            category.save()
        
    return HttpResponse(likes)


#Helper functions
def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
    else:
        cat_list = Category.objects.all()
    
    if max_results > 0:
        if (len(cat_list) > max_results):
            cat_list = cat_list[:max_results]
    for cat in cat_list:
        cat.url = encode(cat.name)
        
    return cat_list


def encode(category_name):
    return category_name.replace(' ','_')


def decode(category_name_url):
    return category_name_url.replace('_',' ')