---
layout: post
title: Welcome to Jekyll!
date: 2016-05-18 20:17:33 +0800
tags: jekyll, update, how-to
---

Creating a static site using Jekyll and Nginx is surprisingly easy, even for 
someone who's just following tutorials on the net. In my case I just followed 
the [Digital Ocean Tutorial][digital-ocean] but I thought I'd quickly summarize
it here for future reference.

## Local Computer 

First, if you don't have a copy of Ruby installed, the easiest way is to use
RVM:

{% highlight bash %}
curl -L https://get.rvm.io | bash -s stable --ruby=2.0.0
{% endhighlight %}

Then install `Jekyll` by grabbing the Jekyll gem:

{% highlight bash %}
gem install jekyll
{% endhighlight %}

Create a new blog:

{% highlight bash %}
jekyll new awesomeblog
{% endhighlight %}

To test that everything was properly setup, you can `cd` into the blog's folder
and use the built in jekyll server. Your static site willl now be available at
[http://localhost:4000/](http://localhost:4000/).

{% highlight bash %}
cd awesomeblog
jekyll serve
{% endhighlight %}

Once you've double checked everything is in working order, you just need to 
make the folder a git repository.

{% highlight bash %}
git init
git add .
git commit -m "Initial commit"
{% endhighlight %}

## On Your Remote Server 

Assuming you already have `git` installed, first you'll need to install Jekyll
like we did on the local computer.

{% highlight bash %}
curl -L https://get.rvm.io | bash -s stable --ruby=2.0.0
gem install jekyll
{% endhighlight %}

Then you create a bare git repo to hold your static site's repository.

{% highlight bash %}
cd ~/
mkdir repos && cd repos  # Make a folder to contain all git repos (optional)
mkdir awesomeblog.git && cd awesomeblog.git
git init --bare
{% endhighlight %}

We're almost done, now you just need to set up a git hook so that whenever you
push anything to the repository on your remote server, it'll automatically 
get Jekyll to compile your static site into html and then copy it to the 
`/var/www/site` directory.

{% highlight bash %}
cd hooks
touch post-receive
vim post-receive
{% endhighlight %}

Make sure to paste this into the `post-receive` file, git will run this every
time it receives a push.

{% highlight bash %}
#!/bin/bash -l
GIT_REPO=$HOME/repos/awesomeblog.git
TMP_GIT_CLONE=$HOME/tmp/git/awesomeblog
PUBLIC_WWW=/var/www/awesomeblog

git clone $GIT_REPO $TMP_GIT_CLONE
jekyll build --source $TMP_GIT_CLONE --destination $PUBLIC_WWW
rm -Rf $TMP_GIT_CLONE
exit 
{% endhighlight %}

[//]: <> $ a random dollar sign because vim-markdown thinks we wrote LaTeX

Now you just need to make the post hook executable (`chmod +x post-receive`) 
and you're finished setting up the Jekyll side of things.

So you can actually make edits locally and push them to your server, you'll 
need to add it as a remote.

{% highlight bash %}
git remote add droplet user@example.org:repos/awesomeblog.git
git git push droplet master
{% endhighlight %}


## Nginx Configuration

Jekyll's built in server is pretty convenient, but I probably wouldn't want to
use it in production, so instead I'll be using Nginx as my actual server.

Nginx has a fairly complete [tutorial][nginx-static] on your basic static 
serving stuff, however it also includes a lot of information we don't really 
need.

First off, make sure you have `nginx` installed. The package in the default
Ubuntu repositories isn't as up to date as it could be, but it should be just
fine for what we're wanting to do. If you want to install the latest release
then there are instructions on the internet.

{% highlight bash %}
sudo apt-get install nginx
{% endhighlight %}

Next `cd` into the `/etc/nginx/` directory. You'll see two directories, one 
called `sites-available` (this is where you store site configurations) and 
`sites-enabled` (configuration files for active sites).

Nginx has the `default` configuration symlinked in `sites-enabled` out of the
box so go and delete that.

{% highlight bash %}
sudo rm /etc/nginx/sites-enabled/default
{% endhighlight %}

Next you'll want to create a new configuration for your site and put it in
`sites-avaliable`.

{% highlight bash %}
sudo vim /etc/nginx/sites-available/blog
{% endhighlight %}

I used the following configuration for my site, it should be fairly intuitive,
so adjust things so they're relevant to your particular setup.

    server {
        listen 80 default_server;
        server_name michaelfbryan.com www.michaelfbryan.com;

        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        root /var/www/blog;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }

Now just tell Nginx to reload its configuration and your static site should 
be ready to go.

{% highlight bash %}
nginx -s reload
{% endhighlight %}

## Some Thoughts

Now that your static site is accessible from the internet, you may want to 
think about a couple other things to make it easier for people to find and to
make the server more secure.

* A DNS registration: Associate your server with a particular domain name (i.e.
  "michaelfbryan.com"). I personally use [GoDaddy][godaddy], but feel free to
  use whatever suits you.
* Firewalls: Ubuntu has a fairly simple firewall that will help to limit the
  number of ways someone can get into your system. Check out [UFW][ufw] for 
  more.


[ufw]: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-14-04
[godaddy]: https://au.godaddy.com/
[digital-ocean]: https://www.digitalocean.com/community/tutorials/how-to-deploy-jekyll-blogs-with-git
[nginx-static]: https://www.nginx.com/resources/admin-guide/serving-static-content/
