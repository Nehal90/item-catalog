from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Category, Base, CategoryItem, User

from flask import session as login_session
from flask import make_response, g, request, redirect, url_for
from functools import wraps

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import AccessTokenCredentials
from oauth2client.client import FlowExchangeError

import random
import string
import httplib2
import json
import requests

from urlparse import urljoin
from flask import request
from werkzeug.contrib.atom import AtomFeed

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Shopping List"

# Connect to Database and create database session

engine = create_engine('sqlite:///catelogitemswithusers.db')

# engine = create_engine('postgres://uiqzqtqlesjzzn:fxAK1ml3_UGwN9YOz70-Y_L66-@ec2-107-20-242-191.compute-1.amazonaws.com:5432/dv91n1mvr0bap')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Authorization Method Starts

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Google+ connect begins here

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    user_id = getUserID(login_session['email'])
    if not user_id:
      user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %  login_session['credentials']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# End of gconnect and gdisconnect

# Facebook connect begins here

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "You have been logged out!"

# End of fbconnect & fb disconnect

# User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None  

def user_authorized_to_edit(category_user_id, login_session_user_id):
    if category_user_id != login_session_user_id:
        flash('You are not authorized to edit this. You can only edit categories and items you have created.')
        return False
    else:
        return True  

def user_authorized_to_delete(category_user_id, login_session_user_id):
    if category_user_id != login_session_user_id:
        flash('You are not authorized to delete this. You can only delete categories and items you have created.')
        return False
    else:
        return True 

def login_required(category_id):
    @wraps(category_id)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('/login', next=request.url))
        return category_id(*args, **kwargs)
    return decorated_function
#####################Authorization Method Ends#####################################################

# Adding Atom feed Endpoints

def make_external(url):
    return urljoin(request.url_root, url)

@app.route('/recent-items.atom')
def recent_feed():
    """
    class name: recent_feed
    endpoint: /recent-items.atom
    Returns: ten most recently added items in atom feed format
    """
    feed = AtomFeed('Recent Ten Items',
                    feed_url=request.url, url=request.url_root)
    items = session.query(CategoryItem).order_by(CategoryItem.item_id.desc()).limit(10)
    for i in items:
        feed.add(i.name, i.description,
                 content_type='text',
                 id=i.item_id,   
                 category=i.category.name,
                 author=i.user.name,
                 updated=i.created_on)
    return feed.get_response()

# Adding JSON Endpoints

@app.route('/categories/JSON')
def categoryJSON():
    """
    class name: categoryJSON
    endpoint: /categories/JSON
    Returns: all categories in easily serializeable format
    """
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])


@app.route('/categories/<int:category_id>/item/JSON')
def categoryItemJSON(category_id):
    """
    class name: categoryJSON
    endpoint: /categories/JSON
    Returns: all categories in easily serializeable format
    """
    category = session.query(Category).filter_by(cid = category_id).one()
    items = session.query(CategoryItem).filter_by(category_id = category_id).all()
    return jsonify(Items=[i.serialize for i in items])
  
@app.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    """
    class name: categoryJSON
    endpoint: /categories/JSON
    Returns: a specific item in easily serializeable format
    """
    categoryItem = session.query(CategoryItem).filter_by(item_id=item_id).one()
    return jsonify(CategoryItem=categoryItem.serialize)

# End of JSON Endpoint definitions

@app.route('/')
@app.route('/categories/')
def categories():
    """
    class name: categories
    desc: Landing page of the website.
    args: None
    returns: all categories available in the database.
    """
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories)


@app.route('/categories/new/', methods=['GET', 'POST'])
@login_required
def newCategory():
    """
    class name: newCategory
    desc: Allows to add a new category in the db.
    args: None
    returns: The categories page with the new category listed.
    """
    if request.method == 'POST':
        newItem = Category(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Category %s Successfully Created' % newItem.name)
        return redirect(url_for('categoryItem', category_id = newItem.cid))
    else:
        return render_template('newcategory.html')

@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    """
    class name: editCategory
    desc: Allows to edit a new category in the db.
    args: category_id (data type: int): the id of the category.
    returns: The categories page with the edited category listed.
    """
    editedCategory = session.query(Category).filter_by(cid = category_id).one()
    if user_authorized_to_edit(editedCategory.user_id, login_session['user_id']):
        if request.method == 'POST':
            if request.form['name']:
                editedCategory.name = request.form['name']
            session.add(editedCategory)
            session.commit()
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('categoryItem', category_id=category_id))
        else:
            return render_template(
                'editcategory.html', category=editedCategory)
    else:
        return redirect(url_for('categoryItem', category_id = category_id))


@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    """
    class name: deleteCategory
    desc: Allows to delete a new category in the db.
    args: category_id (data type: int): the id of the category.
    returns: The categories page with the deleted category NOT listed.
    """
    deletedCategory = session.query(Category).filter_by(cid = category_id).one()

    if user_authorized_to_delete(deletedCategory.user_id, login_session['user_id']):    
        if request.method == 'POST':
            session.delete(deletedCategory)
            session.commit()
            flash('%s Successfully Deleted' % deletedCategory.name)
            return redirect(url_for('categories', category_id = category_id))
        else:
            return render_template(
            'deletecategory.html', category = deletedCategory)
    else:
        return redirect(url_for('categoryItem', category_id = category_id))

@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/item/')
def categoryItem(category_id):
    """
    class name: categoryItem
    desc: Items wihtin a category are listed via this function.
    args: category_id (data type: int): the id of the category.
    returns: all item in a category.
    """
    category = session.query(Category).filter_by(cid = category_id).one()
    creator = getUserInfo(category.user_id)
    items = session.query(CategoryItem).filter_by(category_id = category.cid)
    if 'username' not in login_session:
        return render_template('publicitem.html', items=items, category=category, creator=creator)
    else:
        return render_template('item.html', items=items, category=category, creator=creator)


@app.route('/categories/<int:category_id>/item/new/', methods=['GET', 'POST'])
@login_required
def newItem(category_id):
    """
    class name: newItem
    desc: Allows to add a new item in a category.
    args: category_id (data type: int): the id of the category in which item will be added
    returns: The categories page with the new category listed.
    """
    category = session.query(Category).filter_by(cid=category_id).one()
    if request.method == 'POST':
        newItem = CategoryItem(name=request.form['name'], description=request.form['description'], 
                                category_id=category_id, user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Created' % (newItem.name))
        return redirect(url_for('categoryItem', category_id=category_id))
    else:
        return render_template('newitem.html', category_id=category_id, category = category)


@app.route('/categories/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    """
    class name: editCategory
    desc: Allows to edit a a item.
    args: category_id (data type: int): the id of the category.
          item_id (data type: int): the id of the item.  
    returns: The categories page with the edited item listed in the category.
    """
    category = session.query(Category).filter_by(cid=category_id).one()
    editedItem = session.query(CategoryItem).filter_by(item_id=item_id).one()
    
    if user_authorized_to_edit(editedItem.user_id, login_session['user_id']):
        if request.method == 'POST':
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            session.add(editedItem)
            session.commit()
            flash('Item %s Successfully Edited' % (editedItem.name))
            return redirect(url_for('categoryItem', category_id = category_id))
        else:
            return render_template(
                    'edititem.html', category_id=category_id, item_id=item_id, item=editedItem)
    else:
        return redirect(url_for('categoryItem', category_id = category_id))


@app.route('/categories/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteItem(category_id, item_id):
    """
    class name: deleteItem
    desc: Allows to delete a new category in the db.
    args: category_id (data type: int): the id of the category in which item is listed.
          item_id (data type: int): the id of the item.
    returns: The categories page with the deleted item NOT listed in the category.
    """
    category = session.query(Category).filter_by(cid=category_id).one()
    deletedItem = session.query(CategoryItem).filter_by(item_id=item_id).one()

    if user_authorized_to_delete(deletedItem.user_id, login_session['user_id']):
        if request.method == 'POST':
            session.delete(deletedItem)
            session.commit()
            flash('Item %s Successfully Deleted!' % (deletedItem.name))
            return redirect(url_for('categoryItem', category_id=category_id))
        else:
            return render_template(
               'deleteitem.html', category_id=category_id, item=deletedItem)
    else:
        return redirect(url_for('categoryItem', category_id = category_id))


# Adding Latest Item Functionality
@app.route('/categories/latest-items/')
def latestItems():
    """
    class name: latestItem
    desc: Allows to view last 10 items that got added.
    args: None
    returns: Returns a page with following info about last 10 items added.
                Item name, date and time it was added, the user who added.
    """
    items = session.query(CategoryItem).order_by(CategoryItem.item_id.desc()).limit(10)
    return render_template('latestitems.html', items=items)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully logged out.")
        return redirect(url_for('categories'))
    else:
        flash("You were not logged in!")
        return redirect(url_for('categories'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
app.run(host='0.0.0.0', port=5000)