SERP app
========

**This script is no longer developed with last commits in 2010.**

<img src="https://github.com/mikexstudios/serp/blob/master/screenshots/combined_700x240.png" alt="home">

SERP app (where SERP stands for "Search Engine Results Page") is a search engine
ranking tracking app. Given a website and keywords, this app will track the
ranking of that website for those keywords over time and visualize this data
on a dashboard. 

The goal was to offer this app as a SaaS service for optimizing search engine
ranking. By tracking search ranking for keywords, users can see how specific
changes to their website affect rankings.

## Screenshots

<table>
<tr>
  <td align="center">
   <img src="https://github.com/mikexstudios/serp/blob/master/screenshots/dashboard.png" width="100%">
   <p><strong>Dashboard</strong></p>
  </td>
  <td align="center">
    <img src="https://github.com/mikexstudios/serp/blob/master/screenshots/add.png" width="100%">
    <p><strong>Adding a new link</strong></p>
  </td>
  <td align="center">
    <img src="https://github.com/mikexstudios/serp/blob/master/screenshots/history%20upload-mp3.png" width="100%">
    <p><strong>Ranking history for a link</strong></p>
  </td>
</tr>
</table>

## Usage

1. After cloning this repository, copy `local_settings.py.sample` to 
   `local_settings.py`.

2. Build the `Dockerfile`. Note, this `Dockerfile` uses SQLite and Django's
   development server:

   `docker build -t mikexstudios/serp .`

2. Run it like:

   `docker run -d -p 80:80 mikexstudios/serp`

   If you want to develop while running the script, mount the current 
   directory by:

   ```docker run -d -p 80:80 -v `pwd`:/usr/src/app mikexstudios/serp```

3. Then visit the IP address for the container in your browser. Unfortunately,
   **social logins through Janrain are now broken**. However, you can first
   login through the administration interface at: `http://[ip address]/admin`
   with username: `admin` and password: `pass`. Now that you have established a
   login session, you can bypass all of the social logins. Also, Google search
   ranking retrievals are broken because the AJAX API no longer exists.
