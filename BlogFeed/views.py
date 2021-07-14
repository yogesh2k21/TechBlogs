from django.shortcuts import redirect, render, HttpResponse
from BlogFeed.models import BlogComment, Post
from django.contrib import messages
from django.contrib.auth.models import User
from BlogFeed.templatetags import extras

# Create your views here.
def blogHome(request):
    allposts = Post.objects.all()
    context = {'content': allposts}
    return render(request, 'Blog/blogHome.html', context)


def blogPost(request, slug):  # slug will append in url
    post=Post.objects.filter(slug=slug).first()
    post.views= post.views +1
    post.save()
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'data': post, 'comments': comments, 'user': request.user,'replyDict':replyDict}
    return render(request, 'Blog/blogPost.html', context)


def postComment(request):
    if request.method=="POST":
        comment=request.POST['comment']
        user=request.user
        postSno=request.POST['postSno']
        post=Post.objects.get(sno=postSno)
        parentSno=request.POST['parentSno']
        if parentSno=="":
            comment=BlogComment(comment=comment,user=user,post=post)
            messages.success(request,"Your Comment has been Successfully Posted.")
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            messages.success(request,"Your Reply has been Successfully Posted.")
            
        comment.save()
    return redirect(f"/blog/{post.slug}")


