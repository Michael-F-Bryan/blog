# README

A basic static site created using [pelican][pelican]

## To Use

First install `pelican` and its dependencies:

    pip install pelican markdown

Then `cd` into the project's root directory and generate the html:

    make html

To push to the web server, using rsync:

    make rsync_upload

Or if you want to view it in your browser, start the dev server with:

    ./develop_server.sh start

Then navigate to <http://localhost:8000/>. To stop the server, you need to
run the dev server script again.

    ./develop_server.sh stop


[pelican]: http://blog.getpelican.com/
