from flask_login import current_user, login_required
from flask import render_template, session, redirect, url_for, request, flash

from .. import db
from . import main
from .forms import PostForm
from ..models import User, Post, Category



PER_POSTS_PER_PAGE=8



@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    pagination = \
        Post.query.order_by(Post.timestamp.desc())\
            .paginate(page, per_page=PER_POSTS_PER_PAGE, error_out=False)
    posts = pagination.items
    categorys = Category.query.order_by(Category.count)[::-1]
    return render_template(
        'index.html', posts=posts, pagination=pagination, categorys=categorys)



@main.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    form = PostForm()
    category = Category.query.filter_by(tag=form.category.data).first()
    if form.validate_on_submit():
        if category:
            category.count += 1
            post =\
                Post(title=form.title.data, body=form.body.data,
                     summury=form.summury.data, category=category)
        else:
            post = \
                Post(title=form.title.data, body=form.body.data,
                     summury=form.summury.data,
                     category=Category(tag=form.category.data))
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template("write.html",form=form)



@main.route('/eidt/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.summury = form.summury.data
        db.session.add(post)
        flash('The post has been updated')
        return redirect(url_for('.post', id = post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.summury.data = post.summury
    return render_template('edit_post.html', form=form)



@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.index'))



@main.route('/post/<int:id>', methods=['GET'])
def post(id):
    post=Post.query.get_or_404(id)
    return render_template("post.html",post=post)



@main.route('/category/<tag>', methods=['GET'])
def category(tag):

    category=Category.query.filter_by(tag=tag).first()
    posts=category.posts

    return render_template("category_search.html",posts=posts)



@main.route('/about', methods=['GET'])
def about_website():
    return render_template('about.html')



@main.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
