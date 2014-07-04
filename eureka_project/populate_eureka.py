import os

def populate():
    
    CSIT = add_cat('Computer Science and IT')
    ECE = add_cat("Electronics and Communication")
    EEE = add_cat("Electrical and Electronics")
    EIE = add_cat("Electronics and Instrumentation")
    MECH = add_cat("Mechanical")
    CIVIL = add_cat("Civil")
    VLSI = add_cat("VLSI Design")
    ES = add_cat("Embedded Systems")
    EPE = add_cat("Electrical Power Engineering")
    WMC = add_cat("Wireless and Mobile Communication")
                    
    # Print out what we have added to the user.
    for c in Category.objects.all():
        print "- {0}".format(str(c))

def add_cat(name,views=0,likes=0):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Eureka population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eureka_project.settings')
    from eureka.models import Category
    populate()
