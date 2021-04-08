#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI
import collections
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)



# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
migrate = Migrate(app, db)

# Genres_items = db.Table(
#   'Genres_items',
#   db.Column('Venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
#   db.Column('Genres_id', db.Integer, db.ForeignKey('Genres.id'), primary_key=True)
# )


class Venue_genre(db.Model):
    __tablename__ = 'Venue_genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable = False)

class Artist_genre(db.Model):
    __tablename__ = 'Artist_genre'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable = False)


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key = True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable = False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable = False)
    start_time = db.Column(db.DateTime, nullable = False)
    venue_name = db.Column(db.String(), nullable = False)
    artist_name = db.Column(db.String(), nullable = False)

    def __repr__(self):
        return f'start_time:{self.start_time}'

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    seeking_talent = db.Column(db.Boolean, nullable = False)
    shows = db.relationship('Show', backref = 'Venue', lazy = True)
    genres = db.relationship('Venue_genre', backref = 'Venue', lazy = True)
    # genres_items = db.relationship('Genres', secondary = Genres_items, backref = db.backref('Genres', lazy=True))

    def __repr__(self):
        return f'''
        < id: {self.id}, 
          name: {self.name}, 
          city: {self.city}, 
          state: {self.state}, 
          address: {self.address},
          phone: {self.phone},  
          image_link: {self.image_link},
          facebook_link, {self.facebook_link}
        >'''

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    genres = db.relationship('Artist_genre', backref = 'Artist', lazy = True)
    shows = db.relationship('Show', backref = 'Artist', lazy = True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Real_venue:
    def __init__(self, id, name, num_upcoming_shows):
          self.id = id
          self.name = name
          self.num_upcoming_shows = num_upcoming_shows

    def __repr__(self):
          return f'{self.city}, {self.state}, {self.venues}'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # try:
    locals = []

    exist = False

    try:

      query = Venue.query.distinct(Venue.city, Venue.state)

      places = query.all()

      exist = query is not None

      for place in places:
      # add each local in locals
        venues = Venue.query.filter_by(city = place.city).all()
        
        local = {
            'city': place.city,
            'state': place.state,
            'venues': venues
        }
        locals.append(local)

      print(places)
    
    except:
      return render_template('errors/500.html')
    # data=[{
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "venues": [{
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "num_upcoming_shows": 0,
    #   }, {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "num_upcoming_shows": 1,
    #   }]
    # }, {
    #   "city": "New York",
    #   "state": "NY",
    #   "venues": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }]
    if exist:
      return render_template('pages/venues.html', areas=locals)
    else: 
      return render_template('errors/404.html')

@app.route('/venues/search', methods=['POST'])

def search_venues():
  
  search_term = request.form.get('search_term','')
    
  venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()

  print(venues)

  response = {
    'count': len(venues),
    'data': [{
      'id': venue.id,
      'name': venue.name,
      
    } for venue in venues]
  }


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
  # try:
  #   query = Venue.query.filter_by(name = request.form['search_term'])

  #   exist = query is not None

  #   venues = query.all()

  #   # response={
  #   #   "count": ,
  #   #   "data": [{
  #   #     "id": 2,
  #   #     "name": "The Dueling Pianos Bar",
  #   #     "num_upcoming_shows": 0,
  #   #   }]
  #   # }
  # except:
  #   return render_template('errors/500.html')

  # if exist:

  #   for venue in venues:
  #     response['data'].append({
  #       'id': venue.id,
  #       'name': venue.name,
  #       'num_upcoming_shows': len(venue.shows)
  #     })
  #     response['count'] = query.count()

  #   return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))
  
  # else:
  #  return render_template('errors/404.html')
        

    

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  exist = False

  try:
    venue = Venue.query.get(venue_id) 

    exist = venue is not None

    data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
    }

    current_time = datetime.now()

    upcoming_shows = []

    past_shows = []

    print('test')
    print(venue.shows)

    for show in venue.shows:
      upcoming_shows.append(show) if show.start_time < current_time else past_shows.append(show)

    return render_template('pages/show_venue.html', venue=venue, upcoming_shows = upcoming_shows, past_shows = past_shows)
  except:
    print('error')
    return render_template('errors/500.html')



  if not exist:
    return render_template('errors/404.html')

  
    # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
    # print(data)
  # if len(venue) == 0:
  #   print(venue)
    
  # else:
  #   return render_template('error/404.html')
  
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = request.form

  print(form)
  body = {}
  # on successful db insert, flash success
  try:
    
    # print(form.getlist('genres'))
    venue = Venue(
      name=form['name'], 
      city=form['city'], 
      state=form['state'],
      phone=form['phone'],
      address=form['address'],
      image_link= form['image_link'] if 'image_link' in form else '',
      facebook_link= form['facebook_link'],
      seeking_talent= form['seeking_talent'] if 'seeking_talent' in form else False
    )
    
    

    print('tests')

    genres = []
    
    for g in form.getlist('genres'):
        genre = Venue_genre(name = g, venue_id = venue.id)
        venue.genres.append(genre)
        
        
    # venue.genres = form.getlist('genres')
    db.session.add(venue)

    db.session.commit()

    flash('Venue ' + form['name'] + ' was successfully listed!')

    return redirect(url_for('index'))
  except:
    db.session.rollback()
    flash('Venue ' + 'is not vaild')

    return render_template('errors/500.html')
  finally:
    db.session.close()
    print('venue')
  
  # print(body.venue)

  # TODO: on unsuccessful db insert, flash an error instead.
  
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
      
  
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
      
  exist = False
  
  try:
    query = Artist.query

    exist = query is not None

    artists = query.all()

    data = [{'id': artist.id, 'name': artist.name} for artist in artists]



    # data=[{
    #   "id": 4,
    #   "name": "Guns N Petals",
    # }, {
    #   "id": 5,
    #   "name": "Matt Quevedo",
    # }, {
    #   "id": 6,
    #   "name": "The Wild Sax Band",
    # }]

    return render_template('pages/artists.html', artists=data)
  
  except:
    return render_template('errors/500.html')

  # TODO: replace with real data returned from querying the database

  if not exist:
        return render_template('errors/404.html')
  

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  exist = False

  search_term=request.form.get('search_term', '')

  try:
    artist_query = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

    exist = artist_query is not None

    artists = artist_query.all()
    response={
      "count": len(artists),
      "data": [{
        "id": artist.id,
        "name": artist.name,
        # "num_upcoming_shows": ,
      } for artist in artists]
    }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)
  except:
    return render_template('errors/500.html') 
  
  if not exist:
    return render_template('errors/404.html')
  

  

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  exist = False
  
  try:
    artist = Artist.query.get(artist_id)

    exist = artist is not None

    print(artist.shows)

    data1={
      "id": 4,
      "name": "Guns N Petals",
      "genres": ["Rock n Roll"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "326-123-5000",
      "website": "https://www.gunsnpetalsband.com",
      "facebook_link": "https://www.facebook.com/GunsNPetals",
      "seeking_venue": True,
      "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
      "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "past_shows": [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "start_time": "2019-05-21T21:30:00.000Z"
      }],
      "upcoming_shows": [],
      "past_shows_count": 1,
      "upcoming_shows_count": 0,
    }

    current_time = datetime.now()

    upcoming_shows = []

    past_shows = []

    for show in artist.shows:
      upcoming_shows.append(show) if show.start_time < current_time else past_shows.append(show)

    # upcoming_shows = [show for show in artist.shows]

    # print(len(upcoming_shows))
    for show in artist.shows:
      print(show.start_time)
      

    return render_template('pages/show_artist.html', artist=artist, upcoming_shows = upcoming_shows, past_shows = past_shows)

  except Exception as e:
    print(e)
    return render_template('errors/500.html')

  if not exist:
    return render_template('errors/404.html')

  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
 
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id)

  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes+
  form = request.form

  try:

    artist = Artist.query.get(artist_id)


    artist.name = form['name']                      
    artist.phone = form['phone']
    artist.image_link = form['image_link'] if 'image_link' in form else ''
    artist.facebook_link = form['facebook_link']

    db.session.execute(f'DELETE from "Artist_genre" where artist_id = {artist.id}')
    print('testing')
    for genre in form.getlist('genres'):
      artist.genres.append(
        Artist_genre(name = genre, artist_id = artist.id)
      )
    # artist.city = form['city']
    # artist.state = form['state']

    # name = db.Column(db.String)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    # phone = db.Column(db.String(120))
    # image_link = db.Column(db.String(500))
    # facebook_link = db.Column(db.String(120))


    # for key in artist:
    #       print(key)

    print(dir(artist))

    db.session.commit()

    return redirect(url_for('show_artist', artist_id=artist_id))

  except:
    db.session.rollback()

    return render_template('errors/500.html')

  finally:
    db.session.close()
  


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
      
  form = VenueForm()

  venue = Venue.query.get(venue_id)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

  


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  form = request.form

  exist = False

  try:

    venue = Venue.query.get(venue_id)
    
    exist = venue is not None

    venue.name = form['name']
    venue.city = form['city']
    venue.state = form['state']
    venue.address = form['address']
    venue.phone = form['phone']
    venue.facebook_link = form['facebook_link']

    
  
    # print(dir(db.session))
    db.session.execute(f'DELETE from "Venue_genre" where venue_id = {venue.id}')
    
    for genre in form.getlist('genres'):
      venue.genres.append(Venue_genre(name = genre, venue_id=venue.id))


    print(dir(venue.genres))

    db.session.commit()

    return redirect(url_for('show_venue', venue_id=venue_id))
  except:

    return render_template('errors/500.html')
  
  finally:
    db.session.close()
  
  if not exist:
    return render_template('errors/404.html')
  # venue record with ID <venue_id> using the new attributes
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = request.form

  try:
    print(form)
    artist = Artist(
      name = form['name'],
      city = form['city'],
      state = form['state'],
      phone = form['phone'],
      image_link = form['image_link'] if 'image_link' in form else '',
      facebook_link = form['facebook_link']
    )

    for g in form.getlist('genres'):

      genre = Artist_genre(name = g, artist_id = artist.id)
    
      artist.genres.append(genre)

    print(artist)

    db.session.add(artist)

    db.session.commit()

    flash('Artist ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')
  # on successful db insert, flash success
  except:
    print('test')
    
    db.session.rollback()

    return render_template('errors/500.html')
    
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  finally:
    db.session.close()

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()

  print(shows)

  data = [{
    "venue_id": show.venue_id,
    # "venue_name": show.venue_name,
    "artist_id": show.artist_id,
    # "artist_name": show.artist_name,
    "artist_image_link": None,
    "start_time": show.start_time
  } for show in shows]
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  form = request.form

  try:
    venue = Venue.query.get(form['venue_id'])

    artist = Artist.query.get(form['artist_id'])

    print(form['start_time'])

    dt = datetime.strptime(form['start_time'] ,"%Y-%m-%d %H:%M:%S")

    print(dt)
    
    show = Show(venue_id = venue.id, artist_id = artist.id, start_time = dt, venue_name = venue.name, artist_name = artist.name)

    # print(Show)
    db.session.add(show)
    # venue.shows.append(show)

    print(venue.shows)

    db.session.commit()

    print('commited')

    flash('Show was successfully listed!')

    return render_template('pages/home.html')
  
  except Exception as e:
    db.session.rollback()

    flash(e)

    return render_template('errors/500.html')
  
  finally:
    db.session.close()

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
