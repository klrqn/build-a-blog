import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Blogpost(db.Model):
    title = db.StringProperty(required=True)
    blog_post = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainPage(Handler):
    def renderFront(self, title="", blog_post="", error=""):
        bps = db.GqlQuery("SELECT * FROM Blogpost "
                          "ORDER BY created DESC "
                          "LIMIT 5"
                          )

        self.render("home.html", title=title, blogpost=blog_post, error=error, bps=bps)

    def get(self):
        self.renderFront()

    def post(self):
        title = self.request.get("title")
        blog_post = self.request.get("blog_post")

        if title and blog_post:
            bp = Blogpost(title=title, blog_post=blog_post)
            bp.put()

            self.redirect("/blog")
        else:
            error = "Need to add both a Title and a Blog Post"
            self.renderFront(title, blog_post, error)

class AddPost(Handler):
    #def renderFront(self):
    pass

    #def get(self):



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', MainPage),
], debug=True)
