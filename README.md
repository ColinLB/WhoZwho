WhoZwho
=======

Django based web directory/address book

Installation:

As root:
 1. Install apache, mod_wsgi, mod_ssl.
 2. Install python 2.6.6 or greater.
 3. Install setuptools: curl http://python-distribute.org/distribute_setup.py | python
 4. Install pip: curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python
 5. Install Python Imaging Library: pip install pil
 6. Install django: pip install Django
 7. Install git
 8. Create non-privileged user: adduser my_id

As the non-privileged user ( my_ID ):
 1. Retrieve WhoZwho web directory code: mkdir -i ~/Git; cd ~/Git; git clone git@github.com:ColinLB/WhoZwho.git
 2. Create Django application container: mkdir -p ~/django/my_project; cd ~/django/my_project; django-admin.py startproject my_site
 3. Link application container to code: ln -s ~/Git/WhoZwho
 4. Replace settings.py in the my_site directory with the sample provided in ~/django/my_project/WhoZwho/samples directory. Customize as required, in particular:
      BANNER
      SITENAME
 5. Create apache WhoZwho.conf using sample provided in ~/Git/WhoZwho/samples/apache.conf
 6. Restart apache.

License

This program is free software; you can redistribute it and/or modify it under the terms of either:

a) the GNU General Public License as published by the Free Software Foundation; either version 3, or (at your option) any later version, or

b) the Apache v2 License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See either the GNU General Public License or the Apache v2 License for more details.

You should have received a copy of the Apache v2 License with this software, in the file named "LICENSE".

You should also have received a copy of the GNU General Public License along with this program in the file named "COPYING". If not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA or visit their web page on the internet at http://www.gnu.org/copyleft/gpl.html.
