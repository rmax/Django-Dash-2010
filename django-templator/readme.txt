Django Templator a.k.a. Django TemplateBin

site: http://dash.darkrho.com/
example: http://dash.darkrho.com/c/bdd2f30b00de4101b5239f9865117e32/

This project allows to post collection of django templates 
to render in the server-side. It handles exceptions gracefully.

Requires python 2.6 and django 1.2.

To run:
    - copy local example settings into local directory:
      $ cd templator/conf/local/
      $ cp example/*.py .

    - run the server
      $ ./manage.py runserver

Note: use the given template path in the extends/include tags.
