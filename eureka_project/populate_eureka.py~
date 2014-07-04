import os

def populate():
    
    python_cat = add_cat('Computer Science & IT',128,64)

    add_page(
             cat=python_cat,
             title="Facilitating Effective User Navigation through Website Structure Improvement",
             url="http://docs.python.org/2/tutorial/"
             )
    
    add_page(
             cat=python_cat,
             title="Alice in Warningland: A Large-Scale Field Study of Browser Security Warning Effectiveness",
             url="http://www.greenteapress.com/thinkpython/"
             )
    
    add_page(
             cat=python_cat,
             title="Learn Python",
             url="http://www.korokithakis.net/tutorials/python/"
             )


    django_cat = add_cat("Electronics and Communication",64,32)

    add_page(
             cat=django_cat,
             title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/"
             )

    add_page(
             cat=django_cat,
             title="Django Rocks",
             url="http://www.djangorocks.com/"
             )

    add_page(
             cat=django_cat,
             title="How to Tango with Django",
             url="http://www.tangowithdjango.com/"
             )

    frame_cat = add_cat("Electrical and Electronics",32,16)

    add_page(
             cat=frame_cat,
             title="Automatic knowledge extraction from documents",
             url="http://bottlepy.org/docs/dev/"
             )

    add_page(
             cat=frame_cat,
             title="Flask",
             url="http://flask.pocoo.org"
             )

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name,views=0,likes=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Eureka population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eureka_project.settings')
    from eureka.models import Category, Page
    populate()